import svgwrite
import requests
import base64

COLORS ={
        "NOVICE":"#1fa641",
        "CONTRIBUTOR":"#20c0ff",
        "EXPERT":"#651fff",
        "MASTER":"#ff5c19",
        "GRANDMASTER":"#fae041"
        }

ARCS = {
        "NOVICE":"M 70 15 A 55 55 0 0 1 122.31 53",
        "CONTRIBUTOR":"M 70 15 A 55 55 0 0 1 102.33 114.5",
        "EXPERT":"M 70 15 A 55 55 0 1 1 37.67 114.5",
        "MASTER":"M 70 15 A 55 55 0 1 1 17.69 53",
        "GRANDMASTER":"M 70 15 A 55 55 0 1 1 69.9 15"
        }

WIDTH = 500
IMAGE_XY = (20,20)
IMAGE_BORDER_CENTER = [i+50 for i in IMAGE_XY]
RADIUS = 55


def image(image_url, tier):
    dwg = svgwrite.Drawing()
    dwg.add(dwg.image(f"static/{tier.lower()}.svg", insert = (WIDTH-70, 20), size=(50,50)))
    profile_image = requests.get(image_url)
    img_data = base64.b64encode(profile_image.content).decode('utf-8')

    dwg.add(dwg.circle(center = IMAGE_BORDER_CENTER, r = RADIUS, fill = "#1c1d20", stroke = 'gray', stroke_width=3))

    dwg.add(dwg.path(d=ARCS[tier], fill="none", stroke=COLORS[tier], stroke_width=3))

    mask = dwg.mask(id = 'perfil')
    circle = dwg.circle(center = IMAGE_BORDER_CENTER, r = RADIUS-5, fill ="#ffffff")
    mask.add(circle)
    dwg.add(mask)

    dwg.add(dwg.image(f"data:image/png;base64,{img_data}", insert = IMAGE_XY, size=(100,100), mask = "url(#perfil)"))

    return dwg

def svg(data: dict):
    """
    This function is used to create the svg usign the data from the scrapper, like image, achievements, and tier.
    """
    profile = data['userProfile']
    image_url = profile['userAvatarUrl']
    if 'static' in image_url:
        image_url = 'https://www.kaggle.com'+image_url
    # dibujo

    tier = 'NOVICE' if 'performanceTier' not in profile else profile['performanceTier']



    dwg = svgwrite.Drawing()
    dwg.add(dwg.rect(insert=(0,0), size = (WIDTH,200), rx=40,ry=40, fill = "#1c1d20",stroke=COLORS[tier], stroke_width=3))

    dwg.add(image(image_url, tier))
    # Datos del perfil
    dwg.add(dwg.text(profile['displayName'], insert = (150,50), fill='white'))
    dwg.add(dwg.text(profile['userName'], insert = (150, 80), fill = 'white'))

    for i in "Competitions Kernels Datasets Discussions".split():
        if "total"+i not in profile:
            profile["total"+i] = 0

    dwg.add(dwg.text(f'Competitions: {profile["totalCompetitions"]}', insert = (170, 110), fill = 'white'))
    dwg.add(dwg.text(f'Code: {profile["totalKernels"]}', insert = (170, 130), fill = 'white'))
    dwg.add(dwg.text(f'Datasets: {profile["totalDatasets"]}', insert = (170, 150), fill = 'white'))
    dwg.add(dwg.text(f'Discussions: {profile["totalDiscussions"]}', insert = (170, 170), fill = 'white'))

    return dwg
