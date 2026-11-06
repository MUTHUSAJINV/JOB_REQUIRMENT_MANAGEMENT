import os

path = r'c:\Users\SAJIN\OneDrive\Desktop\job\templates\index.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Canvas element
canvas_html = """
<!-- Interactive Canvas Background -->
<canvas id="bg-canvas"></canvas>
"""
if '<canvas id="bg-canvas">' not in html:
    html = html.replace('<!-- Hero Section -->', canvas_html + '\n<!-- Hero Section -->')

# 2. Add Styles for canvas and neon UI
style_addition = """
#bg-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1;
  background: linear-gradient(to bottom, #040a18, #0a0520);
  pointer-events: auto;
}

.hero-section {
  position: relative;
  z-index: 1;
  background: transparent !important;
}

/* Neon Purple/Cyan UI Accents */
.hero-title {
  text-shadow: 0 0 20px rgba(6, 182, 212, 0.4), 0 0 40px rgba(168, 85, 247, 0.2);
}
.brand-accent {
  background: linear-gradient(135deg, #0ea5e9, #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: none;
}
.hero-pill {
  border: 1px solid rgba(168, 85, 247, 0.4);
  box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);
  background: rgba(16, 22, 38, 0.6) !important;
}
.search-box {
  background: rgba(10, 15, 30, 0.7) !important;
  border: 1px solid rgba(6, 182, 212, 0.3) !important;
  box-shadow: 0 0 25px rgba(6, 182, 212, 0.15) !important;
  backdrop-filter: blur(10px);
}
.stat-card {
  background: rgba(10, 15, 30, 0.6) !important;
  border: 1px solid rgba(168, 85, 247, 0.2) !important;
  backdrop-filter: blur(8px);
}
.btn-primary {
  background: linear-gradient(135deg, #0ea5e9, #a855f7) !important;
  border: none !important;
  box-shadow: 0 0 15px rgba(168, 85, 247, 0.4) !important;
}
.btn-primary:hover {
  box-shadow: 0 0 25px rgba(14, 165, 233, 0.6) !important;
}

/* Scroll Animation Classes */
.scroll-reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.scroll-reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
"""
html = html.replace('</style>', style_addition + '\n</style>')

# Add scroll-reveal class to section elements
html = html.replace('<div class="section-header">', '<div class="section-header scroll-reveal">')
html = html.replace('<div class="job-card">', '<div class="job-card scroll-reveal">')

# 3. Add Canvas JS
js_addition = """
<script>
// --- Canvas Particle/Network System ---
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let width, height;
let particles = [];
let mouse = { x: null, y: null, radius: 150 };

function resize() {
  width = canvas.width = window.innerWidth;
  height = canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

window.addEventListener('mousemove', (e) => {
  mouse.x = e.x;
  mouse.y = e.y;
});
window.addEventListener('mouseout', () => {
  mouse.x = null;
  mouse.y = null;
});

class Particle {
  constructor() {
    this.x = Math.random() * width;
    this.y = Math.random() * height;
    this.size = Math.random() * 2.5 + 0.5;
    this.baseX = this.x;
    this.baseY = this.y;
    this.density = (Math.random() * 30) + 1;
    this.vx = (Math.random() - 0.5) * 0.8;
    this.vy = (Math.random() - 0.5) * 0.8;
    this.color = Math.random() > 0.5 ? '#0ea5e9' : '#a855f7'; // Neon Cyan/Purple
  }
  
  update() {
    this.x += this.vx;
    this.y += this.vy;
    
    if (this.x < 0 || this.x > width) this.vx = -this.vx;
    if (this.y < 0 || this.y > height) this.vy = -this.vy;

    // Mouse interaction (repel)
    if (mouse.x != null) {
      let dx = mouse.x - this.x;
      let dy = mouse.y - this.y;
      let distance = Math.sqrt(dx * dx + dy * dy);
      if (distance < mouse.radius) {
        const forceDirectionX = dx / distance;
        const forceDirectionY = dy / distance;
        const force = (mouse.radius - distance) / mouse.radius;
        const directionX = forceDirectionX * force * this.density;
        const directionY = forceDirectionY * force * this.density;
        this.x -= directionX;
        this.y -= directionY;
      }
    }
  }
  
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.shadowBlur = 10;
    ctx.shadowColor = this.color;
    ctx.fill();
  }
}

function initParticles() {
  particles = [];
  let numberOfParticles = (width * height) / 9000; // density
  for (let i = 0; i < numberOfParticles; i++) {
    particles.push(new Particle());
  }
}

function connect() {
  let maxDistance = 120;
  for (let a = 0; a < particles.length; a++) {
    for (let b = a; b < particles.length; b++) {
      let dx = particles[a].x - particles[b].x;
      let dy = particles[a].y - particles[b].y;
      let distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < maxDistance) {
        let opacity = 1 - (distance / maxDistance);
        ctx.strokeStyle = 'rgba(168, 85, 247,' + opacity * 0.4 + ')';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(particles[a].x, particles[a].y);
        ctx.lineTo(particles[b].x, particles[b].y);
        ctx.stroke();
      }
    }
  }
}

function animate() {
  ctx.clearRect(0, 0, width, height);
  for (let i = 0; i < particles.length; i++) {
    particles[i].update();
    particles[i].draw();
  }
  connect();
  requestAnimationFrame(animate);
}

initParticles();
animate();

// --- Scroll Reveal Observer ---
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.scroll-reveal').forEach((el) => observer.observe(el));
</script>
"""

if '<canvas id="bg-canvas">' not in html:
    pass # Wait, I already added it above. Let's just append JS block.

if 'const canvas = document.getElementById' not in html:
    html = html.replace('{% endblock %}', js_addition + '\n{% endblock %}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Animations added successfully.")