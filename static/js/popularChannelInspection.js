var popularChannelData;
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
        drawBarChartForTop10Anchors(popularChannelData);
        InformationInjection(popularChannelData);
    }
})

// <!--https://dev.twitch.tv/docs/embed/video-and-clips#non-interactive-inline-frames-for-live-streams-and-vods-->

function InformationInjection(popularChannelData) {
    let channelName = popularChannelData["name"];
    document.getElementById("popularChannelSelection").innerHTML = "<select id=\"channelList\">";
    for (let i = 0; i < channelName.length; i++) {
        document.getElementById("popularChannelSelection").innerHTML += "<option value=\"" +
            channelName[i] + "\">" + channelName[i] + "</option>";
    }
    document.getElementById("popularChannelSelection").innerHTML += "</select>";
}

function generateChannelPreview(data) {
    document.getElementById("popularChannelChat").innerHTML = "< iframe\n" +
        "id = \"twitch-chat-embed\"\n" +
        " src = \"https://www.twitch.tv/embed/" +
        data +
        "/chat?parent=proj6893.herokuapp.com\"\n" +
        "height = \"500\"\n" +
        "width = \"350\" >\n" +
        "< /iframe>";
    document.getElementById("popularChannelStream").innerHTML = "<iframe\n" +
        "    src=\"https://player.twitch.tv/?channel=" +
        data +
        "&parent=proj6893.herokuapp.com&muted=true\"\n" +
        "    height=\"720\"\n" +
        "    width=\"1280\"\n" +
        "    allowFullScreen=\"true\">\n" +
        "</iframe>";
}

$(function(){
    // $('.check').trigger('change'); //This event will fire the change event.
    $('.channelList').change(function(){
      let data= $(this).val();
      generateChannelPreview(data);
      alert(data);
    });
});