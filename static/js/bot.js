// Define configuration options
function setUpLink(channelName) {
    let opts = {
        identity: {
            username: "Yhl7",
            password: "8mt1clasptu8nzn0l7dgoonhicom6i"
        },
        channels: [
            channelName
        ]
    };
    const client = new tmi.client(opts);
    client.on('message', onMessageHandler);
    client.on('connected', onConnectedHandler);
    client.connect();
}


// https://rapidapi.com/twinword/api/sentiment-analysis


let sentimentList = [0, 0, 0];
let settings;
let commandName;

// Called every time a message comes in
function onMessageHandler(target, context, msg, self) {
    if (self) {
        return;
    }
    commandName = msg.trim();
    // console.log(commandName);

    settings = {
        "async": true,
        "crossDomain": true,
        "url": "https://twinword-sentiment-analysis.p.rapidapi.com/analyze/?text=" + commandName,
        "headers": {
            "x-rapidapi-host": "twinword-sentiment-analysis.p.rapidapi.com",
            "x-rapidapi-key": "3369bc862cmsh26322dc653e1d9dp120fd5jsn4f6912e00a99"
        }
    };
}

// Called every time the bot connects to Twitch chat
function onConnectedHandler(addr, port) {
    console.log(`* Connected to ${addr}:${port}`);
}


// setInterval(function () {
//     console.log(commandName);
//     $.ajax(settings).done(function (response) {
//         console.log(response);
//         if (sentimentList.reduce((a, b) => a + b, 0) === 1) {
//             let max = 0;
//             let sentiment = "neutral";
//             for (let i = 0; i < sentimentList.length; i++) {
//                 if (sentimentList[i] > max) {
//                     max = sentimentList[i];
//                     if (i === 0) {
//                         sentiment = "Positive";
//                     } else if (i === 1) {
//                         sentiment = "Neutral";
//                     } else {
//                         sentiment = "Negative";
//                     }
//                 }
//             }
//             sentimentList = [0, 0, 0];
//             console.log(sentiment);
//             document.getElementById("sentimentResult").innerHTML = sentiment;
//         } else {
//             if (response.type == "positive") {
//                 sentimentList[0]++;
//             } else if (response.type == "neutral") {
//                 sentimentList[1]++;
//             } else {
//                 sentimentList[2]++;
//             }
//         }
//     });
// }, 5000);


