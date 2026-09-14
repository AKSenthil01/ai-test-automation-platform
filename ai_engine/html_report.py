import html
import os
from datetime import datetime


class HTMLReport:
    """
    Generates a professional HTML report for every AI test generation.
    """

    def __init__(self, output_dir="reports"):

        self.output_dir = output_dir

        os.makedirs(output_dir, exist_ok=True)

    def generate(

            self,

            requirement,

            apis,

            generated_code,

            corrected_code,

            quality,

            execution,

            review,

            output_file="AI_Test_Report.html"

    ):

        path = os.path.join(

            self.output_dir,

            output_file

        )

        score = quality.get("score", 0)

        execution_status = "PASS" if execution.get("success") else "FAIL"

        html_content = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<title>AI Test Generation Report</title>

<style>

body{{
font-family:Arial;
margin:40px;
background:#f4f4f4;
}}

h1{{
color:#1e3d59;
}}

.card{{
background:white;
padding:20px;
margin-bottom:20px;
border-radius:8px;
box-shadow:0px 2px 8px rgba(0,0,0,.15);
}}

pre{{
background:#272822;
color:#f8f8f2;
padding:15px;
overflow:auto;
border-radius:5px;
}}

.pass{{
color:green;
font-weight:bold;
}}

.fail{{
color:red;
font-weight:bold;
}}

table{{
width:100%;
border-collapse:collapse;
}}

td,th{{
padding:8px;
border:1px solid #ddd;
}}

</style>

</head>

<body>

<h1>AI Test Generation Report</h1>

<p><b>Generated:</b> {datetime.now()}</p>

<div class="card">

<h2>Requirement</h2>

<p>{html.escape(requirement)}</p>

</div>

<div class="card">

<h2>Selected Controller APIs</h2>

<ul>

{''.join(f'<li>{html.escape(api)}()</li>' for api in apis)}

</ul>

</div>

<div class="card">

<h2>Quality Score</h2>

<h1>{score}/100</h1>

</div>

<div class="card">

<h2>Execution Status</h2>

<h2 class="{'pass' if execution.get('success') else 'fail'}">

{execution_status}

</h2>

</div>

<div class="card">

<h2>Review Result</h2>

<pre>{html.escape(str(review))}</pre>

</div>

<div class="card">

<h2>Generated Code</h2>

<pre>{html.escape(generated_code)}</pre>

</div>

<div class="card">

<h2>Corrected Code</h2>

<pre>{html.escape(corrected_code)}</pre>

</div>

<div class="card">

<h2>Execution Details</h2>

<pre>{html.escape(str(execution))}</pre>

</div>

</body>

</html>
"""

        with open(

                path,

                "w",

                encoding="utf8"

        ) as f:

            f.write(html_content)

        return path