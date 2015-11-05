The following code was what we wrote in the project tutorial


        @app.route("/hello/", methods=["POST", "GET"])
        def myfirstappfunction():
            print request.args
            print "\n"

            #print request.args["name"]
            print request.args["age"]

            d = dict(title="Ur AGE:"+request.args["age"])
            if int(request.args['age']) < 50:
                return render_template(
                        "index.html", 
                        **d)
            else:
                offset = int(request.args["offset"])
                cursor = g.conn.execute( 
                        "SELECT * FROM test")
                l = []
                for row in cursor:
                    l.append(row[1])
                return render_template(
                        "index.html",
                        title = str(l)
                    )
            return "hello world"


We also created the following simple form in `templates/index.html`

        <html>
        <body>
          <h1>{{title}}</h1>
          <form action="http://w4111db1.cloudapp.net:8111/hello/"
                method="GET">
            age: <input name="age"/><br/>
            offset: <input name="offset"/>
            <input type="submit"/>
          </form>
        </body>
        </html>

We used the following command to run a dead simple HTTP Server on port 8111

        python -m SimpleHTTPServer 8111


We used the following command to run our server.py on port 8111 in
debug mode, which detects when a file has changed and reloads it 
(so you don't need to stop and restart your server all the time)

        python server.py 0.0.0.0 8111 --debug

In order to access our server, we needed to go to the Azure console to
open an Endpoint on our VM.  This is described in the project part 3 description.
