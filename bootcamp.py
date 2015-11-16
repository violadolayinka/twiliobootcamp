from flask import Flask, redirect, url_for

CSS = """
html {
    font-family: sans-serif;
}

#container {
    width: 960px;
    margin: 20px auto;
}

.status {
    border: 1px solid #9a9a9a;
    border-radius: 4px;
    box-shadow: 2px 2px 2px 2px #ababab;
    padding: 30px;
}

.status .identity {
    float: right;
}

.status .indicator {
    float: left;
    border: 10px solid black;
    width: 0px;
    border-radius: 10px;
    margin-right: 10px;
}

.status .indicator.away {
    border-color: #f00;
}

.status .indicator.available {
    border-color: #3f3;
}

.simulator {
    width: 400px;
    margin-top: 20px;
    margin-right: 20px
    border: 1px solid #9a9a9a;
    border-radius: 4px;
    box-shadow: 2px 2px 2px 2px #ababab;
    padding: 30px;
}

.simulator h4 {
    margin-top: 0px;
}

.simulator .input-container {
    margin-bottom: 5px;
}

.simulator label {
    display: inline-block;
    width: 60px;
    text-align: right;
}

.simulator input {
    width: 80%;
}

.simulator .form-action {
    text-align: right;
}

.simulator .form-action input {
    width: auto;
    margin-right: 10px;
}
"""

JS = """
"""

TEMPLATE = """<!DOCTYPE html>
<html>
    <head>
        <title>{title}</title>
        <style type="text/css">
            {css}
        </style>
        <script type="text/javascript">
            {js}
        </script>
    </head>
    <body>
        <div id="container">
            {content}
        </div>
    </body>
</html>
"""

class StudentApp(Flask):
    student_name = None
    available = False
    _message = None
    sms_endpoint = '/sms'

    @property
    def message_html(self):
        return self._message if self._message else '<em>{}</em>'.format('No Message Set')

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message.strip()

    def __init__(self, import_name, static_path=None, static_url_path=None, static_folder='static',
                 template_folder='templates', instance_path=None, instance_relative_config=False):
        self.student_name = import_name
        super(StudentApp, self).__init__(import_name, static_path, static_url_path, static_folder,
                                               template_folder, instance_path, instance_relative_config)

        @self.route('/')
        def dashboard():
            state = 'available' if self.available else 'away'
            content = """
            <div class="status">
                <div class="identity">{name}</div>
                <a href="/toggle-status"><div class="indicator {state}"></div></a> {state} - {message}
            </div>

            <div class="simulator">
                <h4>Message Simulator (POST {sms_endpoint})</h4>
                <form method="post" action="{sms_endpoint}">
                    <div class="input-container">
                        <label for="To">To</label>
                        <input type="text" name="To" id="To" />
                    </div>
                    <div class="input-container">
                        <label for="From">From</label>
                        <input type="text" name="From" id="From" />
                    </div>
                    <div class="input-container">
                        <label for="Body">Body</label>
                        <input type="text" name="Body" id="Body" autocomplete="false" />
                    </div>
                    <div class="form-action">
                        <input type="submit" value="Simulate SMS" />
                    </div>
                </form>
            </div>
            """

            vars = {
                'state': state,
                'message': self.message_html,
                'sms_endpoint': self.sms_endpoint,
                'name': self.student_name,
            }

            return self._render(content.format(**vars))

        @self.route('/toggle-status')
        def toggle_status():
            self.available = not self.available

            return redirect(url_for('dashboard'))



    def route(self, rule, **options):
        if 'methods' not in options:
            options['methods'] = ['GET', 'POST']

        return super(StudentApp, self).route(rule, **options)

    def run(self, host=None, port=None, debug=None, **options):
        if debug is None:
            debug = True

        super(StudentApp, self).run(host, port, debug, **options)

    @staticmethod
    def home():
        return redirect(url_for('dashboard'))


    def display_recordings(self, recordings):
        recordings = recordings['recordings'] # extract payload

        ulist = "<ul>"

        for recording in recordings:
            mp3_uri = "https://api.twilio.com/" + recording['uri'].replace(".json", ".mp3")

            ulist += """<li><a href="{0}">{1}</a></li>""".format(
                mp3_uri, recording['sid']
            )

        return ulist + "</ul>"



    def _render(self, content, css=None, js=None):
        css = '{}\n\n{}'.format(CSS, css) if css else CSS
        js = '{}\n\n{}'.format(JS, js) if js else JS

        return TEMPLATE.format(
            css=css,
            js=js,
            content=content,
            title="{}'s App".format(self.student_name)
        )
