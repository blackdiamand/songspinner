
function loadFile(filePath) {
  var result = null;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", filePath, false);
  xmlhttp.send();
  if (xmlhttp.status==200) {
    result = xmlhttp.responseText;
  }
  return result;
}

var token = "";
(async () => {
  var item = await generateToken();
  token = item.access_token;
})();

async function generateToken (){
  const clientID = loadFile('apikey.txt').split("\n")[0];
  const clientSecret = loadFile('apikey.txt').split("\n")[1];
  const res= await fetch("https://accounts.spotify.com/api/token", {
    method: "POST",
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: `grant_type=client_credentials&client_id=${clientID}&client_secret=${clientSecret}`
  });
  return await res.json();
}


async function fetchWebApi(endpoint, method, body) {
  const res = await fetch(`https://api.spotify.com/${endpoint}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method,
    body:JSON.stringify(body)
  });
  return await res.json();
}

async function searchTracks(searchTerm){
  // Endpoint reference : https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
  return (await fetchWebApi(
      'v1/search?q=' + searchTerm + '&type=track&market=US&limit=50', 'GET'
  ));
}

/*//THE MAIN METHOD!!!
document.getElementById("submitButton").onclick=async() => {
  var textbox = document.getElementById('textbox');
  var searchWord = textbox.value;
  var item = await generateToken();
  token = item.access_token;
  var trackList = await searchTracks(searchWord);
  var outputText = document.getElementById('output');
  //console.log(trackList.tracks.items);
  var randomSong = Math.floor(Math.random() * 20);
  var song = trackList.tracks.items[randomSong];

  var songName = song.album.name;
  var artistName = song.artists[0].name;

  outputText.innerHTML = `<a href='${song.external_urls.spotify}'> ${songName} by ${artistName} </a>`;
};*/

async function geturi(){
  var textbox = document.getElementById('textbox');
  var searchWord = textbox.value;

  var returnWord = loadFile(`./cgi-bin/run.py?input=${searchWord}`);
  var returnWordList = returnWord.split(' ');

  var trackSearchWord = returnWordList[Math.floor(Math.random() * returnWordList.length)];

  //console.log(trackSearchWord);
  var trackList = await searchTracks(trackSearchWord);
  while (!trackSearchWord){
    trackSearchWord = returnWordList[Math.floor(Math.random() * returnWordList.length)];
    trackList = await searchTracks(trackSearchWord);
  }

  var outputText = document.getElementById('output');
  //console.log(trackList.tracks.items);
  var randomSong = Math.floor(Math.random() * 20);
  var song = trackList.tracks.items[randomSong];
  return song.uri;
}


window.onSpotifyIframeApiReady = (IFrameAPI) => {
  const ids = ["embed-iframe0", "embed-iframe1", "embed-iframe2", "embed-iframe3", "embed-iframe4"];
  for (var i = 0; i < 5; i++) {
    const id = ids[i]
    const element = document.getElementById(id);
    const options = {
      width: 270,
      height: 400,
    };
    const callback = (EmbedController) => {
      const submitButton = document.getElementById("submitButton")
      submitButton.addEventListener('click', () => {
        geturi().then(uri => {
          const your_songs = document.getElementById('your_songs');
          your_songs.innerHTML = 'Your songs';
          your_songs.style.visibility = 'visible'
          EmbedController.loadUri(uri);
        });
      });
    };
    IFrameAPI.createController(element, options, callback);
  }
};