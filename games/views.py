from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from .models import Game
from .forms import GameForm, ConfirmDeleteForm
from accounts.utils import is_logged_in
from accounts.models import User


def dashboard(request):
    if not is_logged_in(request):
        return redirect('login')
    games = Game.objects.order_by('-created_at')
    return render(request, 'games/dashboard.html', {'games': games})


def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user = get_object_or_404(User, pk=request.session.get('user_id', None))
            instance.user = user
            form.save()
            messages.success(request, 'Game created successfully.')
            return redirect('games:dashboard')
            # return JsonResponse({
            #     'success': True, 
            #     'redirect_url': reverse('games:dashboard')
            # })
    else:
        form = GameForm()
    return render(request, 'games/game_form.html', {'form': form, 'action': 'Create'})


def game_update(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, 'Game updated successfully.')
            return redirect('games:dashboard')
    else:
        form = GameForm(instance=game)
    return render(request, 'games/game_form.html', {'form': form, 'action': 'Update'})


def game_delete(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = ConfirmDeleteForm(request.POST, game=game)
        if form.is_valid():
            game.delete()
            messages.success(request, 'Game deleted.')
            return redirect('games:dashboard')
    else:
        form = ConfirmDeleteForm(game=game)
    return render(request, 'games/game_confirm_delete.html', {'form': form, 'game': game})

    
def details(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, "games/game_details.html", {
        'game': game,
    })
