// SETUP

var http = require('http'),
    fs = require('fs');

var https = require('https');

var server = http.createServer(function (req, res) {
    console.log("Request for: ", req.url);
    switch (req.url) {
        case '/':
            fs.readFile('./index.html', function(error, data) {
                res.writeHead(200, { 'Content-Type': 'text/html' });
                res.end(data, 'utf-8');
            });
            break;
        case '/css/index.css':
            fs.readFile('./index.css', function(error, data) {
                res.writeHead(200, { 'Content-Type': 'text/css' });
                res.end(data, 'utf-8');
            });
            break;
    }

}).listen(3030, "127.0.0.1");

console.log('Server running at http://127.0.0.1:3030/');

// The above lines of code basically set up a local server for us to access.


var io = require('socket.io').listen(server);
var status = false;

// We are using a package called socket.io.
// Socket.io enables real-time communication between our server and the client.
// Here, the client refers to anyone who accesses our web page.

//



//var nodemailer = require('nodemailer');
//
//// create reusable transporter object using SMTP transport
//var transporter = nodemailer.createTransport({
//    service: 'Gmail',
//    auth: {
//        user: 'willth3rd@gmail.com',
//        pass: 'willthe3rd'
//    }
//});
//
//// NB! No need to recreate the transporter object. You can use
//// the same transporter object for all e-mails
//
//// setup e-mail data with unicode symbols
//var mailOptions = {
//    from: 'Fred Foo ✔ <foo@blurdybloop.com>', // sender address
//    to: 'willth3rd@gmail.com', // list of receivers
//    subject: 'Hello ✔', // Subject line
//    text: 'Hello world ✔', // plaintext body
//    html: '<b>Hello world ✔</b>' // html body
//};
//
//// send mail with defined transport object
//transporter.sendMail(mailOptions, function(error, info){
//    if(error){
//        console.log(error);
//    }else{
//        console.log('Message sent: ' + info.response);
//    }
//});



// HERE'S THE RELEVANT STUFF...

// SECOND, we set a listener to see when someone connects to our web page...
io.sockets.on('connection', function(socket) {

    console.log('New connection made...');

    socket.emit('server_connected');

    socket.on("send_email", function(email_data) {

        console.log(email_data);

        var email_address = email_data[0];
        var body = email_data[1];
        var table = email_data[2];

        var find = '\n';
        var re = new RegExp(find, 'g');

        body = body.replace(re, '<br>');

        var nodemailer = require('nodemailer');
        
        // create reusable transporter object using SMTP transport
        var transporter = nodemailer.createTransport({
           service: 'Gmail',
           auth: {
               user: 'willth3rd@gmail.com',
               pass: 'willthe3rd'
           }
        });
        
        // NB! No need to recreate the transporter object. You can use
        // the same transporter object for all e-mails
        
        // setup e-mail data with unicode symbols
        var mailOptions = {
           from: 'Fred Foo ✔ <foo@blurdybloop.com>', // sender address
           to: email_address, // list of receivers
           subject: 'Hello ✔', // Subject line
           text: 'Hello world ✔', // plaintext body
           html: body + "<br><br><br><br><br>" + table // html body
        };
        
        // send mail with defined transport object
        transporter.sendMail(mailOptions, function(error, info){
           if(error){
               console.log(error);
           }else{
               console.log('Message sent: ' + info.response);
               socket.emit("email_success");
           }
        });






    });

    socket.on("updatedData", function(updatedData) {

        console.log(updatedData);
        console.log(updatedData[0]);

        var datasetID;
        for(var id in updatedData){
            console.log(id + ": "+ updatedData[id]);
            datasetID = id.split(" ").slice(0,2);
            datasetID = datasetID[1] + " " + datasetID[0];
            // console.log(datasetID[1] + " " + datasetID[0]);
            break;
        }

        console.log(datasetID);

        fs = require('fs');
        fs.writeFile("" + datasetID, JSON.stringify(updatedData), function (err, data) {
          if (err) {
            return console.log(err);
          } else {
              console.log("Data saved successfully.");

          }
        });

    });

    socket.on("get_file", function(seeking) {

        console.log("get file plz");

        seeking = seeking.split(" ")[1] + " " + seeking.split(" ")[0];

        var path = seeking;

        fs = require('fs');
        if (fs.existsSync(path)) {
            console.log("" + seeking);
        } else {
            console.log("File not found.");
        }

        var PythonShell = require('python-shell');
 
        var options = {
          args: [seeking]
        };
         
        PythonShell.run('json_to_xml.py', options, function (err, results) {
          if (err) throw err;
          // results is an array consisting of messages collected during execution 
          console.log('results: %j', results);
          socket.emit("got_file", seeking + ".xml");
        });

    });

    socket.on('get_data', function() {

        console.log("Got request for data.");

        var PythonShell = require('python-shell');
        var fs = require('fs');

        PythonShell.run('retrieve_data.py', function (err) {

            fs.readFile('table/data.json', 'utf8', function (err, data) {
              if (err) {
                return console.log(err);
              }
              console.log(data);

              socket.emit('table_data', data);

            });

            if (err) throw err;
            console.log('Finished getting JSON.');
            socket.emit('xml_rendered');
        });

    });

    socket.on('new_data', function(data) {

        console.log(data);

    });

    socket.on('send_data', function(data) {

        console.log('Got data.');

        socket.emit('server_got_data');

        console.log(data);
        console.log(data.data);
        var data = data.data;
        console.log(data);

        var parsedData = JSON.parse(data);
        console.log(parsedData);

        var fs = require('fs');
        fs.writeFile("data.json", JSON.stringify(parsedData), function(err) {
            if(err) {
                console.log(err);
            } else {
                console.log("The file was saved!");

                var PythonShell = require('python-shell');

                PythonShell.run('json_to_xml.py', function (err) {
                    if (err) throw err;
                    console.log('Finished rendering XML file.');
                    socket.emit('xml_rendered');
                });
            }
        });

    });
    // print to the console that the connection has been made


    // THIRD, once a connection has been established, we send an 'initialize' message back to the page.
    socket.emit('initialize');
    console.log('Initialized.');


});
