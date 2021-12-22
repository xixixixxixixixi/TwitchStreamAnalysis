let popularChannelData;
$.ajax({
    url: domain + "/getChannelStreamSchedule/" + 10,
    type: 'GET',
    cache: false,
    processData: false,
    contentType: 'application/json',
    success: function (r) {
        console.log(r)
        popularChannelData = JSON.parse(r);
        console.log(popularChannelData);
        InformationInjection(popularChannelData);
    }
})

// <!--https://dev.twitch.tv/docs/embed/video-and-clips#non-interactive-inline-frames-for-live-streams-and-vods-->

function InformationInjection(popularChannelData) {
    let channelName = popularChannelData["name"];
    let channelListString = "";
    for (let i = 0; i < channelName.length; i++) {
        channelListString += "<option value=\"" +
            channelName[i] + "\">" + channelName[i] + "</option>";
    }
    document.getElementById("popularChannelSelection").innerHTML = "<select id=\"channelList\">" +
        channelListString + "</select>";
    // for (let i = 0; i < channelName.length; i++) {
    //     document.getElementById("popularChannelSelection").innerHTML += "<option value=\"" +
    //         channelName[i] + "\">" + channelName[i] + "</option>";
    // }
    document.getElementById("popularChannelSelection").innerHTML += "<button id=\"goToChannel\" " +
        "onClick=\"changeChannel()\">change channel</button>";
    generateChannelPreview($('#channelList').val());
}

function changeChannel() {
    let channel = $('#channelList').val();
    generateChannelPreview(channel);
    setUpLink(channel);

    setInterval(function () {
        console.log(commandName);
        $.ajax(settings).done(function (response) {
            console.log(response);
            document.getElementById("sentimentResult").innerHTML = response.type;
        });
    }, 5000);
}

//
// $('#channelList').change(function(){
//     var data= $(this).val();
//     alert(data);
//     generateChannelPreview(data);
// });

function generateChannelPreview(data) {
    document.getElementById("popularChannelChat").innerHTML = "" +
        "<iframe id=\"twitch-chat-embed\"" +
        " src=\"https://www.twitch.tv/embed/" +
        data +
        "/chat?parent=proj6893.herokuapp.com\"" +
        " height=\"500\"" +
        " width=\"350\">" +
        "</iframe>"
    document.getElementById("popularChannelStream").innerHTML = "<iframe\n" +
        "    src=\"https://player.twitch.tv/?channel=" +
        data +
        "&parent=proj6893.herokuapp.com&muted=true\"\n" +
        "    height=\"720\"\n" +
        "    width=\"1248\"\n" +
        "    allowFullScreen=\"true\">\n" +
        "</iframe>";
}
