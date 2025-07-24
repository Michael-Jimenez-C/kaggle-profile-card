import svgwrite
import requests
import base64
from datetime import datetime

# Configuración de colores y estilos
COLORS = {
    "NOVICE": "#1fa641",
    "CONTRIBUTOR": "#20c0ff", 
    "EXPERT": "#651fff",
    "MASTER": "#ff5c19",
    "GRANDMASTER": "#fae041"
}

ARCS = {
    "NOVICE": "M 70 15 A 55 55 0 0 1 122.31 53",
    "CONTRIBUTOR": "M 70 15 A 55 55 0 0 1 102.33 114.5",
    "EXPERT": "M 70 15 A 55 55 0 1 1 37.67 114.5",
    "MASTER": "M 70 15 A 55 55 0 1 1 17.69 53",
    "GRANDMASTER": "M 70 15 A 55 55 0 1 1 69.9 15"
}

# Configuración del layout rediseñado
CARD_WIDTH = 600
CARD_HEIGHT = 300
CARD_PADDING = 20
TOP_PADDING = 35  # Padding adicional desde el borde superior
AVATAR_SIZE = 80
AVATAR_RADIUS = AVATAR_SIZE // 2

# Posiciones
AVATAR_X = CARD_PADDING + AVATAR_RADIUS
AVATAR_Y = TOP_PADDING + AVATAR_RADIUS  # Usar el padding superior
CONTENT_X = AVATAR_X + AVATAR_RADIUS + 20

# Iconos monocromáticos minimalistas
ICONS = {
    "competitions": "●",  # Círculo sólido
    "notebooks": "■",     # Cuadrado sólido
    "datasets": "▲",      # Triángulo sólido
    "discussions": "◆",   # Rombo sólido
    "location": "▼",      # Triángulo hacia abajo
    "calendar": "◐",      # Círculo medio lleno
    "github": "◎",        # Círculo con punto
    "linkedin": "▣",      # Cuadrado con líneas
    "followers": "◯",     # Círculo vacío
    "badge": "★",         # Estrella
    "organization": "◈"   # Rombo con punto para organización
}

# Colores para los iconos
ICON_COLORS = {
    "competitions": "#ffd700",  # Dorado para competiciones
    "notebooks": "#20c0ff",     # Azul para code/notebooks
    "datasets": "#1fa641",      # Verde para datasets
    "discussions": "#ff5c19",   # Naranja para discussions
    "location": "#ccc",         # Gris claro para ubicación
    "calendar": "#ccc",         # Gris claro para fecha
    "github": "#4fb3ff",        # Azul para GitHub
    "linkedin": "#4fb3ff",      # Azul para LinkedIn
    "followers": "#ccc",        # Gris claro para followers
    "badge": "#ffd700",         # Dorado para badges
    "organization": "#651fff"   # Morado para organización
}

# Compatibilidad con código anterior
WIDTH = CARD_WIDTH
IMAGE_XY = (AVATAR_X - AVATAR_RADIUS, AVATAR_Y - AVATAR_RADIUS)
IMAGE_BORDER_CENTER = [AVATAR_X, AVATAR_Y]
RADIUS = AVATAR_RADIUS


def lighten_color(hex_color, factor):
    """Aclara un color hexadecimal"""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    rgb = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def darken_color(hex_color, factor):
    """Oscurece un color hexadecimal"""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    rgb = tuple(max(0, int(c * (1 - factor))) for c in rgb)
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def format_date(date_string):
    """Formatea una fecha ISO a un formato más legible"""
    try:
        date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date.strftime("%B %Y")
    except:
        return "N/A"

def get_main_achievement_tier(profile):
    """Obtiene el tier principal del usuario"""
    if 'performanceTier' in profile:
        return profile['performanceTier']
    return 'NOVICE'

def create_profile_image(dwg, image_url, tier):
    """Crea la imagen de perfil circular con borde del tier"""
    try:
        profile_image = requests.get(image_url, timeout=10)
        img_data = base64.b64encode(profile_image.content).decode('utf-8')
        
        # Círculo de fondo
        dwg.add(dwg.circle(
            center=(AVATAR_X, AVATAR_Y), 
            r=AVATAR_RADIUS + 3, 
            fill="#1c1d20", 
            stroke='gray', 
            stroke_width=2
        ))
        
        # Máscara circular para la imagen
        mask = dwg.mask(id='profile-mask')
        circle = dwg.circle(
            center=(AVATAR_X, AVATAR_Y), 
            r=AVATAR_RADIUS - 2, 
            fill="#ffffff"
        )
        mask.add(circle)
        dwg.add(mask)
        
        # Imagen de perfil
        dwg.add(dwg.image(
            f"data:image/jpeg;base64,{img_data}",
            insert=(AVATAR_X - AVATAR_RADIUS, AVATAR_Y - AVATAR_RADIUS),
            size=(AVATAR_SIZE, AVATAR_SIZE),
            mask="url(#profile-mask)"
        ))
        
        # Arco del tier - colocado después de la imagen para que esté encima
        # Calcular la transformación correcta para centrar el arco en la nueva posición
        scale_factor = AVATAR_RADIUS / 55
        offset_x = AVATAR_X - (70 * scale_factor)
        offset_y = AVATAR_Y - (70 * scale_factor)
        
        arc_transform = f"translate({offset_x}, {offset_y}) scale({scale_factor})"
        dwg.add(dwg.path(
            d=ARCS[tier], 
            fill="none", 
            stroke=COLORS[tier], 
            stroke_width=3,
            transform=arc_transform
        ))
        
    except Exception as e:
        print(f"Error loading profile image: {e}")
        # Círculo de placeholder si falla la imagen
        dwg.add(dwg.circle(
            center=(AVATAR_X, AVATAR_Y),
            r=AVATAR_RADIUS,
            fill="#666",
            stroke=COLORS[tier],
            stroke_width=3
        ))

def add_tier_badge(dwg, tier):
    """Agrega el badge del tier en la esquina superior derecha"""
    badge_x = CARD_WIDTH - 60
    badge_y = TOP_PADDING + 5  # Usar el padding superior más un pequeño offset
    
    # Icono del tier
    try:
        dwg.add(dwg.image(
            f"static/{tier.lower()}.svg",
            insert=(badge_x, badge_y),
            size=(40, 40)
        ))
    except:
        # Fallback a texto si no hay icono
        dwg.add(dwg.text(
            tier,
            insert=(badge_x, badge_y + 20),
            fill=COLORS[tier],
            font_size="12px",
            font_weight="bold"
        ))

def add_header_info(dwg, profile, tier):
    """Agrega la información del header (nombre, username)"""
    y_pos = AVATAR_Y - 25  # Ajustar posición con el nuevo padding
    
    # Nombre principal
    dwg.add(dwg.text(
        profile.get('displayName', 'Unknown User'),
        insert=(CONTENT_X, y_pos),
        fill='white',
        font_size="24px",
        font_weight="bold",
        font_family="Arial, sans-serif"
    ))
    
    # Username
    y_pos += 25
    dwg.add(dwg.text(
        f"@{profile.get('userName', 'unknown')}",
        insert=(CONTENT_X, y_pos),
        fill='#888',
        font_size="16px",
        font_family="Arial, sans-serif"
    ))

def add_stats_section(dwg, profile):
    """Agrega la sección de estadísticas con iconos"""
    stats_y = AVATAR_Y + 30  # Desplazar 10 píxeles hacia abajo (era +20, ahora +30)
    stats = [
        ('competitions', profile.get('totalCompetitions', 0)),
        ('notebooks', profile.get('totalKernels', 0)),
        ('datasets', profile.get('totalDatasets', 0)),
        ('discussions', profile.get('totalDiscussions', 0))
    ]
    
    # Crear dos columnas
    for i, (stat_type, value) in enumerate(stats):
        x_pos = CONTENT_X + (i % 2) * 150
        y_pos = stats_y + (i // 2) * 25
        
        # Icono con color específico
        dwg.add(dwg.text(
            ICONS[stat_type],
            insert=(x_pos, y_pos),
            font_size="14px",
            fill=ICON_COLORS[stat_type]
        ))
        
        # Texto
        dwg.add(dwg.text(
            f"{stat_type.title()}: {value}",
            insert=(x_pos + 20, y_pos),
            fill='white',
            font_size="13px",
            font_family="Arial, sans-serif"
        ))

def add_location_info(dwg, profile):
    """Agrega información de ubicación, fecha y organización"""
    info_y = AVATAR_Y + 90  # Ajustar también para mantener el espaciado proporcional
    
    # Ubicación
    location_parts = []
    if profile.get('city'): location_parts.append(profile['city'])
    if profile.get('country'): location_parts.append(profile['country'])
    
    if location_parts:
        location = ", ".join(location_parts)
        dwg.add(dwg.text(
            ICONS['location'],
            insert=(CONTENT_X, info_y),
            font_size="12px",
            fill=ICON_COLORS['location']
        ))
        dwg.add(dwg.text(
            location,
            insert=(CONTENT_X + 18, info_y),
            fill='#ccc',
            font_size="12px",
            font_family="Arial, sans-serif"
        ))
        info_y += 20
    
    # Organización
    organizations = profile.get('organizations', [])
    if organizations and len(organizations) > 0:
        org_name = organizations[0].get('name', '')
        if org_name:
            dwg.add(dwg.text(
                ICONS['organization'],
                insert=(CONTENT_X, info_y),
                font_size="12px",
                fill=ICON_COLORS['organization']
            ))
            dwg.add(dwg.text(
                org_name,
                insert=(CONTENT_X + 18, info_y),
                fill='#ccc',
                font_size="12px",
                font_family="Arial, sans-serif"
            ))
            info_y += 20
    
    # Fecha de registro
    join_date = format_date(profile.get('userJoinDate', ''))
    dwg.add(dwg.text(
        ICONS['calendar'],
        insert=(CONTENT_X, info_y),
        font_size="12px",
        fill=ICON_COLORS['calendar']
    ))
    dwg.add(dwg.text(
        f"Member since {join_date}",
        insert=(CONTENT_X + 18, info_y),
        fill='#ccc',
        font_size="12px",
        font_family="Arial, sans-serif"
    ))

def add_social_links(dwg, profile):
    """Agrega enlaces sociales si están disponibles"""
    social_y = CARD_HEIGHT - 40
    x_pos = CONTENT_X
    
    # GitHub
    if profile.get('gitHubUserName'):
        dwg.add(dwg.text(
            ICONS['github'],
            insert=(x_pos, social_y),
            font_size="12px",
            fill=ICON_COLORS['github']
        ))
        dwg.add(dwg.text(
            profile['gitHubUserName'],
            insert=(x_pos + 18, social_y),
            fill='#4fb3ff',
            font_size="11px",
            font_family="Arial, sans-serif"
        ))
        x_pos += 120

def add_achievements_info(dwg, profile):
    """Agrega información sobre achievements"""
    achievements = profile.get('achievementSummaries', [])
    if not achievements:
        return
    
    # Posición en la esquina inferior derecha
    badge_x = CARD_WIDTH - 150
    badge_y = CARD_HEIGHT - 60
    
    dwg.add(dwg.text(
        f"{ICONS['badge']} {len(profile.get('badges', []))} Badges",
        insert=(badge_x, badge_y),
        fill='#ffd700',
        font_size="12px",
        font_weight="bold",
        font_family="Arial, sans-serif"
    ))
    
    # Mostrar el mejor ranking
    best_rank = min(achievement.get('rankOutOf', float('inf')) for achievement in achievements)
    if best_rank != float('inf'):
        dwg.add(dwg.text(
            f"Best Rank: {best_rank:,}",
            insert=(badge_x, badge_y + 15),
            fill='#ccc',
            font_size="10px",
            font_family="Arial, sans-serif"
        ))

def svg(data: dict):
    """
    Función principal para crear el SVG rediseñado con toda la información del perfil
    """
    profile = data['userProfile']
    tier = get_main_achievement_tier(profile)
    
    # Crear el drawing con el nuevo tamaño
    dwg = svgwrite.Drawing(size=(CARD_WIDTH, CARD_HEIGHT))
    
    # Fondo principal con gradiente sutil
    dwg.add(dwg.rect(
        insert=(0, 0),
        size=(CARD_WIDTH, CARD_HEIGHT),
        rx=15, ry=15,
        fill="#1a1a1a",
        stroke=COLORS[tier],
        stroke_width=2
    ))
    
    # Barra superior con color del tier
    dwg.add(dwg.rect(
        insert=(0, 0),
        size=(CARD_WIDTH, 8),
        rx=15, ry=15,
        fill=COLORS[tier]
    ))
    
    # Imagen de perfil
    image_url = profile['userAvatarUrl']
    if 'static' in image_url:
        image_url = 'https://www.kaggle.com' + image_url
    
    create_profile_image(dwg, image_url, tier)
    
    # Badge del tier
    add_tier_badge(dwg, tier)
    
    # Información del header
    add_header_info(dwg, profile, tier)
    
    # Estadísticas
    add_stats_section(dwg, profile)
    
    # Información de ubicación y fecha
    add_location_info(dwg, profile)
    
    # Enlaces sociales
    add_social_links(dwg, profile)
    
    # Información de achievements
    add_achievements_info(dwg, profile)
    
    return dwg
