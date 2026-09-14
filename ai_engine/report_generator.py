import os

from datetime import datetime


class ReportGenerator:

    def __init__(self):

        os.makedirs("reports", exist_ok=True)

    def generate(
            self,
            requirement,
            generated_code,
            review,
            quality,
            metrics
    ):

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = os.path.join(
            "reports",
            f"report_{timestamp}.html"
        )

        html = f"""
<html>

<head>

<title>AI Test Automation Report</title>

<style>

body {{
font-family: Arial;
margin:40px;
}}

pre {{

background:#f4f4f4;

padding:15px;

border-radius:5px;

}}

table {{

border-collapse: collapse;

width:100%;

}}

td,th {{

border:1px solid #ddd;

padding:8px;

}}

th {{

background:#007ACC;

color:white;

}}

</style>

</head>

<body>

<h1>AI Test Automation Report</h1>

<h2>Requirement</h2>

<p>{requirement}</p>

<h2>Generated Code</h2>

<pre>{generated_code}</pre>

<h2>Review</h2>

<pre>{review}</pre>

<h2>Quality Score</h2>

<h3>{quality}/100</h3>

<h2>Metrics</h2>

<table>

<tr>

<th>Metric</th>

<th>Value</th>

</tr>

"""

        for key, value in metrics.items():

            html += f"""
<tr>

<td>{key}</td>

<td>{value}</td>

</tr>
"""

        html += """

</table>

</body>

</html>

"""

        with open(
                filename,
                "w",
                encoding="utf8"
        ) as f:

            f.write(html)

        return filename