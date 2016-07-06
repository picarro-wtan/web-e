import flask

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import JS_RESOURCES, CSS_RESOURCES
from bokeh.util.string import encode_utf8
from bokeh.models import DatetimeTickFormatter

app = flask.Flask(__name__)

colors = {
    'Black': '#000000',
    'Red':   '#FF0000',
    'Green': '#00FF00',
    'Blue':  '#0000FF',
}

js_resources = JS_RESOURCES.render(
    js_raw=INLINE.js_raw,
    js_files=INLINE.js_files
)

css_resources = CSS_RESOURCES.render(
    css_raw=INLINE.css_raw,
    css_files=INLINE.css_files
)

@app.route("/")
def plot_data():
    # get data
    x = []
    y = []
    colors = []
    i = 0
    with open("time_dep.csv", "r") as f:
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            items = line.split(',')
            x.append(float(items[0]))
            y.append(float(items[1]))
            
    fig = figure(title="Taxi trips versus Day", plot_width=600, plot_height=400, x_axis_type="datetime", toolbar_location="below")
    fig.line(x, y)
    fig.xaxis[0].formatter = DatetimeTickFormatter(formats=dict(days=["%a"]))
    fig.yaxis.axis_label = 'Number of Trips'

    script, div = components(fig, INLINE)
    html = flask.render_template(
        'layout.html', #'layout.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)
    
if __name__ == "__main__":
    app.run(debug=True)