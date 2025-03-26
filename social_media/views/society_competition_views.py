from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from social_media.forms import CustomisationForm, PostForm, EventCreationForm, DeleteRoleForm, SocietyRoleForm
from social_media.models.colour_history import SocietyColorHistory
from social_media.models import Society, Event, Membership, EventsParticipant, Competition,CompetitionParticipant, SocietyRole, User, Match
from django.utils.timezone import now
from datetime import date, datetime
from django.http import JsonResponse
from social_media.helpers import redirect_to_society_dashboard
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from social_media.forms.competition_creation_form import CompetitionForm
from django.core.exceptions import ValidationError
from django.db.models import Max
from social_media.helpers import *


@login_required
@committee_required
def create_competition(request, society_id):
    """Create a new competition for the given society."""
    if request.method == "POST":
        form = CompetitionForm(request.POST)
        if form.is_valid():
            competition = form.save(commit=False)
            competition.society_id = society_id
            competition.save()
            messages.success(request, "Competition created successfully.")
            return redirect("manage_competitions", society_id=society_id)    
        else:
            messages.error(request, "Invalid competition details. Please check the form.")
    else:
        form = CompetitionForm()
    return render(request, "society/competitions/create_competition.html", {"form": form, "society_id": society_id})


@login_required
@committee_required
def manage_competitions(request, society_id):
    society = get_object_or_404(Society, pk=society_id)
    competitions = Competition.objects.filter(society=society)

    return render(
        request,
        "society/competitions/manage_competitions.html",
        {
            "society_id": society_id,
            "society": society,
            "competitions": competitions,
        }
    )

@login_required
@committee_required
def finalize_competition(request, society_id, competition_id):
    """Allows for finalizing lineup so no new joins/leaves."""
    competition = get_object_or_404(Competition, pk=competition_id)
    
    if competition.is_ongoing: 
        competition.is_finalized = True
        competition.save()
    else:
        messages.error(request,"You cannot modify an ended competition")
    return redirect("competition_details", competition_id=competition_id)

@login_required
def competition_details(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    society = competition.society

    user_membership = Membership.objects.filter(user=request.user, society=society).first()
    is_admin = bool(user_membership and user_membership.is_committee_member())

    participant = CompetitionParticipant.objects.filter(
        user=request.user, competition=competition
    ).first()

    if competition.is_point_based:
        all_parts = competition.participants.order_by("-points")
    else:
        all_parts = competition.participants.order_by("user__username")

    uneliminated_parts = competition.participants.filter(is_eliminated=False)

    if not competition.is_point_based:
        latest_winner_ids = set()
        latest_round = competition.matches.aggregate(Max("round_number"))["round_number__max"]
        if latest_round:
            latest_matches = competition.matches.filter(round_number=latest_round, is_finished=True)
            for match in latest_matches:
                if match.winner_participant:
                    latest_winner_ids.add(match.winner_participant.id)
    else:
        latest_winner_ids = None

    if request.method == "POST":
        action = request.POST.get("action")

        if is_admin:
            if action == "toggle_elimination":
                if competition.is_ongoing:
                    part_id = request.POST.get("participant_id")
                    part = get_object_or_404(CompetitionParticipant, pk=part_id, competition=competition)
                    part.is_eliminated = not part.is_eliminated
                    part.save()
                else:
                    messages.error(request,"You cannot modify an ended competition")
                return redirect("competition_details", competition_id=competition_id)
            
            elif action == "end_competition":
                competition.is_ongoing = False
                competition.save()
                return redirect("competition_details", competition_id=competition_id)
    
    context = {
        "competition": competition,
        "is_admin": is_admin,
        "is_participant": bool(participant),
        "participant": participant,
        "all_participants": all_parts,
        "uneliminated_parts": uneliminated_parts,
        "latest_winner_ids": latest_winner_ids,
    }

    return render(request, "society/competitions/competition_details.html", context)

@login_required
@committee_required
def set_up_round(request, society_id, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    if not competition.is_finalized:
        return HttpResponseForbidden("Cannot set up new matches. Competition is not finalized yet.")

    
    available_parts = CompetitionParticipant.objects.filter(competition=competition, is_eliminated=False)

    last_round = competition.matches.filter(is_finished=True).aggregate(Max("round_number"))["round_number__max"]
    round_number = last_round + 1 if last_round else 1  

    existing_matches = Match.objects.filter(competition=competition, round_number=round_number)

    selected_participants = set()
    for match in existing_matches:
        if match.participant1:
            selected_participants.add(match.participant1.id)
        if match.participant2:
            selected_participants.add(match.participant2.id)
       
        available_parts = available_parts.exclude(id__in=selected_participants)

    match_rows = []

    if request.method == "POST":
        for i in range(1):
            match_rows.append(i)
        action = request.POST.get("action")

        if action == "add_match":
            scheduled_time = request.POST.get("scheduled_time")
            i = 0
            while True:
                opp1_key = f"match_{i}_participant1"
                opp2_key = f"match_{i}_participant2"


                if opp1_key not in request.POST or opp2_key not in request.POST:
                    break  # no more match forms in POST data

                opp1_id = request.POST.get(opp1_key)
                opp2_id = request.POST.get(opp2_key)
                i += 1

                # Skip if either is blank or if they're the same
                if not opp1_id or not opp2_id or opp1_id == opp2_id:
                    continue
                
                if Match.objects.filter(
                    competition=competition,
                    round_number=round_number,
                    participant1_id=opp1_id,
                    participant2_id=opp2_id
                ).exists():
                    continue

                match_data = {
                    "competition": competition,
                    "round_number": round_number,
                }
                if scheduled_time:
                    try:
                        match_data["scheduled_time"] = datetime.fromisoformat(scheduled_time)
                    except ValueError:
                        pass

                match_data["participant1_id"] = opp1_id
                match_data["participant2_id"] = opp2_id
                

                match = Match(**match_data)
                try:
                    match.clean()
                    match.save()
                except ValidationError as e:
                    print("Error creating match:", e.messages)

            return redirect("set_up_round", society_id=competition.society.id, competition_id=competition_id)

        elif action == "revert_match":
            match_id = request.POST.get("match_id")
            match = get_object_or_404(Match, pk=match_id)
            match.delete()
            return redirect("set_up_round", society_id=competition.society.id, competition_id=competition.id)

    if request.method == "GET" or request.POST.get("add_match"):
        for i in range(1):
            match_rows.append(i)

    context = {
        "competition": competition,
        "available_parts": available_parts,
        "round_number": round_number,
        "match_rows": match_rows,
        "existing_matches": existing_matches,
    }
    context["uneliminated_parts"] = competition.participants.filter(is_eliminated=False)


    return render(request, "society/competitions/set_up_round.html", context)


@login_required
def record_match_results(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)

    # find latest round
    latest_round = competition.matches.aggregate(Max("round_number"))["round_number__max"] or 0
    if latest_round == 0:
        return redirect("competition_details", competition_id=competition_id)

    matches_in_round = (Match.objects
        .filter(competition=competition, round_number=latest_round)
        .select_related("participant1", "participant2"))

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "eliminate":
            eliminate_id = request.POST.get("eliminate_participant_id")
            if eliminate_id:
                part = get_object_or_404(CompetitionParticipant, pk=eliminate_id, competition=competition)
                part.is_eliminated = True
                part.save()
            return redirect("record_match_results", competition_id=competition_id)


        elif action == "update_points" and competition.is_point_based:
            for match in matches_in_round:
                # old scores
                old_p1 = match.score_p1 or 0.0
                old_p2 = match.score_p2 or 0.0

                # get new scores
                score_p1_str = request.POST.get(f"score_p1_{match.id}")
                score_p2_str = request.POST.get(f"score_p2_{match.id}")
                
                if score_p1_str and score_p2_str:
                    try:
                        new_p1 = float(score_p1_str)
                        new_p2 = float(score_p2_str)
                    except ValueError:
                        continue
                    
                    match.score_p1 = new_p1
                    match.score_p2 = new_p2
                    
                    # update participant’s total points
                    delta_p1 = new_p1 - old_p1
                    delta_p2 = new_p2 - old_p2

                    if match.participant1:
                        match.participant1.points += delta_p1
                    if match.participant2:
                        match.participant2.points += delta_p2

                    match.is_finished = True
                    match.save()
                    if match.participant1:
                        match.participant1.save()
                    if match.participant2:
                        match.participant2.save()
                        
            return redirect("record_match_results", competition_id=competition_id)

        elif action == "pick_winner" and not competition.is_point_based:
            for match in matches_in_round:
                winner_id = request.POST.get(f"winner_{match.id}")
                if winner_id:
                    if str(match.participant1_id) == winner_id:
                        match.winner_participant_id = match.participant1_id
                    elif str(match.participant2_id) == winner_id:
                        match.winner_participant_id = match.participant2_id
                    match.is_finished = True
                match.save()
            return redirect("record_match_results", competition_id=competition_id)

    all_finished = all(m.is_finished for m in matches_in_round)

    context = {
        "competition": competition,
        "round_number": latest_round,
        "matches_in_round": matches_in_round,
        "all_finished": all_finished,
        "uneliminated_parts": competition.participants.filter(is_eliminated=False),
    }
    return render(request, "society/competitions/record_match_results.html", context)
