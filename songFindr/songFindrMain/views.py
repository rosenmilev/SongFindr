import re
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView

from .forms import SearchForm
import requests

GENIUS_API_KEY = "lOZIJZuK-MrLZR_RM3g7Pb4Pt_Ufsij1qZxw-QIgGTr3zfJzFFUi6h9eE2aORbZc"


def search_songs(word):
	base_url = "https://api.genius.com"
	headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
	search_url = f"{base_url}/search"
	params = {"q": word}
	response = requests.get(search_url, params=params, headers=headers)
	json = response.json()
	song_info = []
	pattern = re.compile(re.escape(word), re.IGNORECASE)

	def bold_replace(match):
		return f'<strong>{match.group()}</strong>'

	for hit in json["response"]["hits"]:
		if word.lower() in hit["result"]["title"].lower() or word.lower() in hit["result"]["primary_artist"][
			"name"].lower():
			title = pattern.sub(bold_replace, hit["result"]["title"])
			artist = pattern.sub(bold_replace, hit["result"]["primary_artist"]["name"])
			song_info.append((title, artist))
	return song_info


def index(request):
	form = SearchForm()
	return render(request, 'index.html', {'form': form})


def results(request):
	form = SearchForm(request.POST)
	if form.is_valid():
		word = form.cleaned_data['word']
		songs = search_songs(word)
		songs = [(mark_safe(title), mark_safe(artist)) for title, artist in songs]
		nothing_found = not bool(songs)
		return render(request, 'results_page.html', {'songs': songs, 'nothing_found': nothing_found, 'form': form})
	else:
		return redirect('index')


class TermsOfUseView(TemplateView):
	template_name = 'terms_of_use.html'
