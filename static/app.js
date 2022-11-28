// document.getElementById("test").innerHTML = "Working";

async function getTestData()
{
    data = JSON.stringify({
                symbol:"NSE:SBIN-EQ",
                resolution:"D",
                date_format:"0",
                range_from:"1622097600",
                range_to:"1622097685",
                cont_flag:"1"
            });
    var received_data = await fetchData('test/', data);

    console.log(await received_data);

    document.getElementById("test3").innerHTML = "NEWWWW " + JSON.stringify(await received_data);


//    fetch('test/', {
//        method: 'POST',
//        body: data,
//        headers: { 'Accept': 'application/json, text/plain, */*',
//            'Content-Type': 'application/json'
//            },
//    })
//    .then(response => response.json())
//    .then((data1) => {
//        console.log(data1)
//        document.getElementById("test3").innerHTML = "NEWWWW " + JSON.stringify(data1);
//    })
//    .catch(function(error) {
//      console.log(error);
//    });
}



function myfunction() {
alert("how are you");
}

function getData()
{
    newTest();
    document.getElementById("test2").innerHTML += "<br/>" + new Date().toLocaleTimeString();
    requested_data = JSON.stringify({
                symbol:document.getElementById("symbol").value,
                resolution:document.getElementById("resolution").value,
                date_format:document.getElementById("date_format").value,
                range_from:document.getElementById("range_from").value,
                range_to:document.getElementById("range_to").value,
                cont_flag:document.getElementById("cont_flag").value
            })

    fetch('getdata/', {
        method: 'POST',
        body: requested_data,
        headers: { 'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
            },
    })
    .then(response => response.json())
    .then((received_data) => {
        console.log(received_data)
        if(received_data["response"]["candles"] != null)
        {
            var candles = received_data["response"]["candles"];

            for(let i = 0; i < candles.length; i++)
            {
                console.log("Total Candles:- " + candles.length);
                //Convert epoch to locale date time format
                candles[i][0] = new Date(JSON.stringify(candles[i][0]) * 1000).toLocaleString();
                document.getElementById("test2").innerHTML += "<br/>" + JSON.stringify(candles[i]);
                for(let j = 0; j < candles[i].length; j++)
                {
//                    document.getElementById("test2").innerHTML += "<br/>" + JSON.stringify(candles[i][j]);
                }
            }
            document.getElementById("test2").innerHTML += "<br/>" + new Date().toLocaleTimeString();
        }
        else
        {
            alert(received_data["response"]["message"]);
        }
    })
    .catch(function(error) {
      console.log(error);
    });
}

var now = new Date();
var milliSecondsTillExucution = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 9, 46, 0, 0) - now;
console.log(milliSecondsTillExucution);
if (milliSecondsTillExucution < 0)
{
    //If the execution time has already been passed
    console.log("TIME PASSED ALREADY")
    checkFile();

     //milliSecondsTillExucution += 86400000; // it's after 10am, try 10am tomorrow.
}
else
{
    setTimeout(executeTrade, milliSecondsTillExucution);
}


async function checkFile()
{
    var received_data = await fetchData('check_file/', '');

    console.log(await received_data);
    if(await JSON.stringify(received_data.response) == 0)
    {
        document.getElementById("test3").innerHTML = "NO TRADE" ;
    }
    else if(await JSON.stringify(received_data.response) == 1)
    {
        document.getElementById("test3").innerHTML = "ORDERS ALREADY PLACED" ;
        setOrderExitFunction();
    }
}


async function executeTrade()
{
    data = JSON.stringify({
                symbol:"NSE:NIFTYBANK-INDEX"
            });
//    var received_data = await fetchData('execute_trade/', data);
//
//    console.log(await received_data);

    fetch('execute_trade/', {
        method: 'POST',
        body: data,
        headers: { 'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
            },
    })
    .then(response => response.json())
    .then((received_data) => {
        console.log(received_data)
        document.getElementById("test3").innerHTML = "NEWWWW " + JSON.stringify(received_data);

        if(received_data["response"]["response"] == 0)
        {
            document.getElementById("test2").innerHTML = "ORDERS PLACED NOW" ;
            setOrderExitFunction();
        }
        else if(received_data["response"]["response"] == 1)
        {
            document.getElementById("test2").innerHTML = "ORDERS ALREADY PLACED" ;
        }
    })
    .catch(function(error) {
      console.log(error);
    });
}


function setOrderExitFunction()
{
    var now = new Date();
    var milliSecondsTillExucution = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 3, 5, 0, 0) - now;
    console.log(milliSecondsTillExucution);
    if (milliSecondsTillExucution < 0)
    {
        //If the execution time has already been passed

         //milliSecondsTillExucution += 86400000; // it's after 10am, try 10am tomorrow.
    }
    else
    {
        setTimeout(exitTrade, milliSecondsTillExucution);
    }
}

async function exitTrade()
{
    data = JSON.stringify({
                symbol:"NSE:NIFTYBANK-INDEX"
            });
//    var received_data = await fetchData('execute_trade/', data);
//
//    console.log(await received_data);

    fetch('exit_trade/', {
        method: 'POST',
        body: data,
        headers: { 'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
            },
    })
    .then(response => response.json())
    .then((received_data) => {
        console.log(received_data)
        document.getElementById("test3").innerHTML = "NEWWWW " + JSON.stringify(received_data);

        if(received_data["response"]["response"] == 1)
        {
            document.getElementById("test2").innerHTML = "FILE NOT FOUND" ;
        }
        else if(received_data["response"]["response"] == 0)
        {
            document.getElementById("test2").innerHTML = "ORDERS EXIED SUCCESSFULLY" ;
        }
    })
    .catch(function(error) {
      console.log(error);
    });
}


async function fetchData(functionName, requested_data)
{
    data = requested_data;

    let response = await fetch(functionName , {
        method: 'POST',
        body: data,
        headers: { 'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
            },
    })
    .catch(function(error) {
      console.log(error);
    });


    return await response.json();
//    .then(response => response.json())
//    .then((received_data) => {
//        console.log(received_data)
//        return received_data;
//    })
//    .catch(function(error) {
//      console.log(error);
//      return;
//    });
}