
#VISUALISATIONS FOR all sites
html_header="""
<head>
<title>PControlDB</title>
<meta charset="utf-8">
<meta name="keywords" content="Wind Energy Dashboard">
<meta name="description" content="project control dashboard">
<meta name="author" content="Joel Ntihemuka, styling greatly influenced by Larry Prato">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<h1 style="font-size:300%; color:#008080; font-family:Georgia"> WIND FARM ENERGY  <br>
<h2 style="color:#008080; font-family:Georgia"> DASHBOARD</h3> <br>
<hr style= "  display: block;
margin-top: 0.5em;
margin-bottom: 0.5em;
margin-left: auto;
margin-right: auto;
border-style: inset;
border-width: 1.5px;"></h1>
"""


html_card_header1="""
<div class="card">
<div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 350px;
height: 50px;">
    <h3 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;"> Last Output </h3>
</div>
</div>
"""
html_card_footer1="""
<div class="card">
<div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 350px;
height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;"></p>
</div>
</div>
"""
html_card_header2="""
<div class="card">
<div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 350px;
height: 50px;">
    <h3 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Current Output</h3>
</div>
</div>
"""

html_card_header3="""
<div class="card">
<div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 350px;
height: 50px;">
    <h3 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;"> Next Hour Forecast</h3>
</div>
</div>
"""
html_card_footer3="""
<div class="card">
<div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 350px;
height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;"></p>
</div>
</div>
"""

html_card_header4="""
<div class="card">
<div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 10px; width: 250px;
height: 50px;">
    <h5 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 5px 0;">RMSE</h5>
</div>
</div>
"""
html_card_footer4="""
<div class="card">
<div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 250px;
height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Model Accuracy measure</p>
</div>
</div>
"""
html_card_header5="""
<div class="card">
<div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 250px;
height: 50px;">
    <h5 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 8px 0;">MAPE</h5>
</div>
</div>
"""
html_card_footer5="""
<div class="card">
<div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 250px;
height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Model Accuracy Measure</p>
</div>
</div>
"""


html_card_header6="""
<div class="card">
<div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 250px;
height: 50px;">
    <h3 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 8px 0;">Inputs</h3>
</div>
</div>
"""
html_card_footer6="""
<div class="card">
<div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 250px;
height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Model Accuracy Measure</p>
</div>
</div>
"""

html_card_header7="""
<div class="card">
<div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #eef9ea; padding-top: 5px; width: 250px;
height: 50px;">
    <h3 class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 8px 0;">Forecast</h3>
</div>
</div>
"""
html_card_footer7="""
<div class="card">
<div class="card-body" style="border-radius: 0px 0px 10px 10px; background: #eef9ea; padding-top: 1rem;; width: 250px;
height: 50px;">
    <p class="card-title" style="background-color:#eef9ea; color:#008080; font-family:Georgia; text-align: center; padding: 0px 0;">Possible output</p>
</div>
</div>
"""


html_list="""
<ul style="color:#008080; font-family:Georgia; font-size: 15px">
<li>Nulla volutpat aliquam velit</li>
<li>Maecenas sed diam eget risus varius blandit</li>
<li>Etiam porta sem malesuada magna mollis euismod</li>
<li>Fusce dapibus, tellus ac cursus commodo</li>
<li>Maecenas sed diam eget risus varius blandit</li>
</ul> 
    """


html_line="""
<br>
<br>
<br>
<br>
<hr style= "  display: block;
margin-top: 0.5em;
margin-bottom: 0.5em;
margin-left: auto;
margin-right: auto;
border-style: inset;
border-width: 1.5px;">
<p style="color:Gainsboro; text-align: right;">By: ntihemukajoel@gmail.com</p>
"""