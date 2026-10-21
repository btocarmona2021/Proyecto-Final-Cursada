<template>
  <div class="home">
    <a class="skip-link" href="#contenido">Ir al contenido</a>
    <header class="home-header">
      <div class="home-container header-inner">
        <RouterLink to="/" class="brand" aria-label="VetSystem, inicio">
          <img
            :src="urlImagen(clinica?.logo) || `${base}vetsystem.svg`"
            style="object-fit: contain"
            alt=""
            width="42"
            height="42"
          />
          <span>Patitas del Sur<small>Clínica veterinaria</small></span>
        </RouterLink>
        <nav class="home-nav" aria-label="Navegación principal">
          <a href="#servicios" class="section-link">Servicios</a>
          <a href="#contacto" class="section-link">Contacto</a>
          <RouterLink
            v-if="auth.estaAutenticado"
            :to="destinoPanel"
            class="home-button button-small"
            >Ir a mi panel</RouterLink
          >
          <RouterLink v-else to="/login" class="home-button button-small"
            >Iniciar sesión</RouterLink
          >
        </nav>
      </div>
    </header>

    <main id="contenido">
      <section class="hero" aria-labelledby="titulo-principal">
        <div class="home-container hero-grid">
          <div class="hero-copy">
            <p class="clinic-name">{{ clinica?.nombre_fantasia || 'Bienvenido a VetSystem' }}</p>
            <h1 id="titulo-principal">Su bienestar,<br />más cerca.</h1>
            <p class="hero-description">
              Los turnos, las vacunas y la historia clínica de tu mascota, en un mismo lugar. Más
              simple para vos, más cuidado para ellos.
            </p>
            <div class="hero-actions">
              <RouterLink :to="destinoPrincipal" class="home-button">{{
                auth.estaAutenticado && !auth.esCliente ? 'Ir a mi panel' : 'Reservar un turno'
              }}</RouterLink>
              <RouterLink v-if="!auth.estaAutenticado" to="/registro" class="text-link"
                >Crear mi cuenta</RouterLink
              >
              <a v-else href="#servicios" class="text-link">Ver los servicios</a>
            </div>
            <p v-if="!auth.estaAutenticado" class="hero-hint">
              Ingresá con tu cuenta para reservar un turno.
            </p>
          </div>
          <figure class="hero-art">
            <img
              :src="`${base}veterinaria.png`"
              alt="Veterinaria con un perro y un gato en la clínica Patitas del Sur"
              width="1374"
              height="1145"
              fetchpriority="high"
            />
            <figcaption>Una historia de cuidado, juntos.</figcaption>
          </figure>
        </div>
      </section>

      <div class="home-container care-strip" aria-label="Qué podés hacer en VetSystem">
        <p>
          <span aria-hidden="true">✚</span><strong>Atención veterinaria</strong
          ><span>Servicios para su salud</span>
        </p>
        <p>
          <span aria-hidden="true">◷</span><strong>Turnos desde tu cuenta</strong
          ><span>Organizá su próxima visita</span>
        </p>
        <p>
          <span aria-hidden="true">♡</span><strong>Su historia, a mano</strong
          ><span>Consultas y vacunas registradas</span>
        </p>
      </div>

      <section
        id="servicios"
        class="home-container home-section"
        aria-labelledby="titulo-servicios"
      >
        <div class="section-heading">
          <div>
            <h2 id="titulo-servicios">Cuidarlos en cada etapa.</h2>
            <p>Conocé los servicios de la clínica y prepará su próxima visita.</p>
          </div>
          <a href="#contacto" class="text-link">Consultar con la clínica</a>
        </div>
        <div :aria-busy="cargandoServicios">
          <p v-if="cargandoServicios" class="home-state" role="status">
            Cargando servicios de la clínica…
          </p>
          <div v-else-if="errorServicios" class="home-state" role="alert">
            <p>No pudimos cargar los servicios. Podés volver a intentarlo.</p>
            <button type="button" class="text-link retry-button" @click="cargarServicios">
              Reintentar
            </button>
          </div>
          <p v-else-if="servicios.length === 0" class="home-state">
            La clínica todavía no publicó sus servicios. Consultá los datos de contacto más abajo.
          </p>
          <ul v-else class="service-list">
            <li v-for="servicio in servicios" :key="servicio.id" class="service-item">
              <div class="service-description">
                <h3>{{ servicio.nombre }}</h3>
                <p v-if="servicio.descripcion">{{ servicio.descripcion }}</p>
                <span class="service-duration"
                  >Duración estimada: {{ servicio.duracion_estimada }} min</span
                >
              </div>
              <span class="service-price">{{ precio(servicio.precio) }}</span>
            </li>
          </ul>
        </div>
      </section>

      <section class="visit-section" aria-labelledby="titulo-visita">
        <div class="home-container visit-grid">
          <div>
            <h2 id="titulo-visita">Tu próxima visita<br />empieza acá.</h2>
            <p>Unos pasos sencillos para empezar a usar tu cuenta.</p>
          </div>
          <ol class="visit-steps">
            <li>
              <span aria-hidden="true">1</span>
              <div>
                <h3>Creá tu cuenta</h3>
                <p>Registrate con tus datos para acceder al espacio de tus mascotas.</p>
              </div>
            </li>
            <li>
              <span aria-hidden="true">2</span>
              <div>
                <h3>La clínica registra a tu mascota</h3>
                <p>El equipo la vincula con tu cuenta para que puedas consultar su información.</p>
              </div>
            </li>
            <li>
              <span aria-hidden="true">3</span>
              <div>
                <h3>Reservá y seguí su atención</h3>
                <p>Elegí un turno y consultá las atenciones y vacunas que registre la clínica.</p>
              </div>
            </li>
          </ol>
        </div>
      </section>

      <section
        id="contacto"
        class="home-container home-section contact-grid"
        aria-labelledby="titulo-contacto"
      >
        <div>
          <img
            v-if="clinica?.logo"
            :src="urlImagen(clinica.logo)"
            :alt="`Logo de ${clinica.nombre_fantasia || clinica.razon_social}`"
            class="contact-logo"
          />
          <p class="clinic-name">
            {{ clinica?.nombre_fantasia || clinica?.razon_social || 'Nuestra clínica' }}
          </p>
          <h2 id="titulo-contacto">Estamos para<br />acompañarte.</h2>
          <p class="contact-description">
            {{
              clinica?.descripcion ||
              'Consultá con la clínica para conocer más sobre la atención de tu mascota.'
            }}
          </p>
        </div>
        <p v-if="cargandoClinica" class="home-state" role="status">
          Cargando información de contacto…
        </p>
        <div v-else-if="errorClinica" class="home-state" role="alert">
          <p>No pudimos cargar la información de contacto.</p>
          <button type="button" class="text-link retry-button" @click="cargarClinica">
            Reintentar
          </button>
        </div>
        <dl v-else-if="clinica" class="contact-details">
          <div>
            <dt>Dónde estamos</dt>
            <dd>{{ direccion || 'Consultá la dirección con la clínica.' }}</dd>
          </div>
          <div>
            <dt>Horario de atención</dt>
            <dd>{{ clinica.horario_atencion || 'Consultá los horarios con la clínica.' }}</dd>
          </div>
          <div v-if="clinica.telefono">
            <dt>Teléfono</dt>
            <dd>
              <a :href="`tel:${clinica.telefono.replace(/[^\d+]/g, '')}`">{{ clinica.telefono }}</a>
            </dd>
          </div>
          <div v-if="clinica.email">
            <dt>Email</dt>
            <dd>
              <a :href="`mailto:${clinica.email}`">{{ clinica.email }}</a>
            </dd>
          </div>
        </dl>
        <p v-else class="home-state">
          Los datos de contacto estarán disponibles cuando la clínica complete su información.
        </p>
      </section>
    </main>

    <footer class="home-footer">
      <div class="home-container footer-inner">
        <span class="footer-brand">VetSystem</span>
        <p>El cuidado de tu mascota, en un solo lugar.</p>
        <small>© {{ anioActual }} VetSystem</small>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { urlImagen } from '@/utils/imagenes'
import { ref, computed, onMounted, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import serviciosService from '@/services/serviciosService'
import veterinariaService from '@/services/veterinariaService'
import type { Servicio } from '@/interfaces/servicioInterface'
import type { Veterinaria } from '@/interfaces/veterinariaInterface'

const auth = useAuthStore()
const base = import.meta.env.BASE_URL
const servicios = ref<Servicio[]>([])
const clinica = ref<Veterinaria | null>(null)
watch(
  clinica,
  (datos) => {
    document.title = datos?.nombre_fantasia?.trim() || datos?.razon_social?.trim() || 'VetSystem'
  },
  { immediate: true },
)
const cargandoServicios = ref(true)
const cargandoClinica = ref(true)
const errorServicios = ref(false)
const errorClinica = ref(false)
const anioActual = new Date().getFullYear()
const destinoPanel = computed(() =>
  auth.esCliente ? { name: 'ClienteInicio' } : { name: 'Agenda' },
)
const destinoPrincipal = computed(() =>
  auth.esCliente
    ? { name: 'ClienteReservar' }
    : auth.estaAutenticado
      ? { name: 'Agenda' }
      : { name: 'Login' },
)
const direccion = computed(() =>
  [clinica.value?.direccion, clinica.value?.ciudad, clinica.value?.provincia]
    .filter(Boolean)
    .join(', '),
)
const moneda = new Intl.NumberFormat('es-AR', {
  style: 'currency',
  currency: 'ARS',
  minimumFractionDigits: 0,
  maximumFractionDigits: 2,
})
const precio = (valor: string | number) =>
  Number.isFinite(Number(valor)) ? moneda.format(Number(valor)) : 'Consultar'

async function cargarServicios() {
  cargandoServicios.value = true
  errorServicios.value = false
  try {
    servicios.value = (await serviciosService.obtenerTodos()).filter((servicio) => servicio.activo)
  } catch {
    errorServicios.value = true
  } finally {
    cargandoServicios.value = false
  }
}

async function cargarClinica() {
  cargandoClinica.value = true
  errorClinica.value = false
  try {
    clinica.value = (await veterinariaService.obtenerTodos())[0] ?? null
  } catch {
    errorClinica.value = true
  } finally {
    cargandoClinica.value = false
  }
}

onMounted(() => Promise.all([cargarServicios(), cargarClinica()]))
</script>

<style scoped>
.home {
  --green: #198754;
  --pine: #153c34;
  --ink: #18332e;
  --muted: #52695f;
  --mint: #eaf5ef;
  --line: #d8e5dc;
  color: var(--ink);
  background: #fff;
  font-family: 'Segoe UI', system-ui, sans-serif;
}
.home-container {
  width: min(1120px, calc(100% - 64px));
  margin-inline: auto;
}
.home a {
  text-decoration: none;
}
.home a:focus-visible,
.home button:focus-visible {
  outline: 3px solid #b06b13;
  outline-offset: 5px;
}
.skip-link {
  position: absolute;
  top: -100px;
  left: 20px;
  z-index: 10;
  background: white;
  padding: 12px;
  color: var(--pine);
}
.skip-link:focus {
  top: 12px;
}
.home-header {
  background: white;
  border-bottom: 1px solid var(--line);
}
.header-inner {
  min-height: 94px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--pine);
  font-size: 25px;
  font-weight: 750;
  line-height: 1.15;
}
.brand small {
  display: block;
  color: var(--muted);
  font-size: 12px;
  font-weight: 400;
  margin-top: 5px;
}
.home-nav {
  display: flex;
  gap: 32px;
  align-items: center;
}
.section-link {
  color: var(--muted);
  font-size: 15px;
  padding-block: 12px;
}
.section-link:hover {
  color: var(--green);
}
.home-button {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  padding: 15px 25px;
  min-height: 48px;
  border-radius: 8px;
  color: #fff;
  background: var(--green);
  font-weight: 650;
  font-size: 15px;
}
.home-button:hover {
  background: #12663f;
  color: white;
}
.button-small {
  padding: 11px 20px;
}
.hero {
  background: var(--mint);
}
.hero-grid {
  display: grid;
  grid-template-columns: 1.08fr 1fr;
  align-items: center;
  gap: 40px;
  padding-block: 64px 58px;
}
.clinic-name {
  color: #286047;
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 18px;
}
.home h1,
.home h2 {
  font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
  letter-spacing: -0.045em;
  color: var(--pine);
  font-weight: 700;
}
.home h1 {
  font-size: clamp(44px, 5.2vw, 70px);
  line-height: 1.06;
  margin: 0 0 24px;
}
.hero-description {
  max-width: 440px;
  font-size: 18px;
  line-height: 1.7;
  color: var(--muted);
  margin-bottom: 28px;
}
.hero-actions {
  display: flex;
  align-items: center;
  gap: 25px;
  flex-wrap: wrap;
}
.text-link {
  color: var(--pine);
  font-weight: 600;
  font-size: 15px;
  text-decoration: underline !important;
  text-underline-offset: 5px;
}
.text-link:hover {
  color: var(--green);
}
.hero-hint {
  font-size: 12px;
  color: var(--muted);
  margin: 14px 0 0;
}
.hero-art {
  margin: 0;
  text-align: center;
}
.hero-art img {
  display: block;
  width: 100%;
  height: auto;
  max-height: 400px;
  object-fit: cover;
  border-radius: 20px;
}
.hero-art figcaption {
  font-size: 13px;
  color: var(--muted);
  margin-top: 12px;
}
.care-strip {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  padding-block: 30px;
  border-bottom: 1px solid var(--line);
  gap: 24px;
}
.care-strip p {
  display: grid;
  grid-template-columns: 34px 1fr;
  column-gap: 10px;
  margin: 0;
}
.care-strip p > span:first-child {
  grid-row: span 2;
  color: var(--green);
  font-size: 28px;
  line-height: 1.3;
}
.care-strip strong {
  font-weight: 600;
  font-size: 14px;
}
.care-strip p > span:last-child {
  color: var(--muted);
  font-size: 12px;
  margin-top: 5px;
}
.home-section {
  padding-block: 78px;
  scroll-margin-top: 24px;
}
.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 24px;
  margin-bottom: 34px;
}
.home h2 {
  font-size: clamp(30px, 3.2vw, 42px);
  line-height: 1.18;
  margin-bottom: 16px;
}
.section-heading p,
.visit-grid > div > p,
.contact-logo {
  display: block;
  width: 150px;
  max-width: 100%;
  height: 110px;
  object-fit: contain;
  object-position: left center;
  margin-bottom: 20px;
}
.contact-description {
  color: var(--muted);
  font-size: 16px;
  line-height: 1.8;
  margin: 0;
  max-width: 480px;
}
.section-heading > .text-link {
  flex-shrink: 0;
  margin-bottom: 6px;
}
.service-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  column-gap: 42px;
}
.service-item {
  border-top: 1px solid var(--line);
  padding: 25px 0;
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 20px;
}
.service-item h3 {
  font-size: 18px;
  font-weight: 650;
  line-height: 1.45;
  margin: 0 0 8px;
}
.service-description {
  min-width: 0;
  overflow-wrap: anywhere;
}
.service-item p {
  font-size: 14px;
  line-height: 1.7;
  color: var(--muted);
  margin: 0 0 12px;
}
.service-price {
  color: var(--green);
  white-space: nowrap;
  font-weight: 700;
  font-size: 17px;
  padding-top: 3px;
}
.service-duration {
  color: var(--muted);
  font-size: 12px;
}
.home-state {
  padding: 24px;
  background: var(--mint);
  border-radius: 8px;
  color: var(--muted);
  line-height: 1.7;
  margin: 0;
}
.home-state p {
  margin-bottom: 10px;
}
.retry-button {
  border: 0;
  padding: 5px 0;
  background: transparent;
}
.visit-section {
  background: #f5f8f5;
  padding-block: 62px;
}
.visit-grid {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  gap: 90px;
  align-items: start;
}
.visit-steps {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 28px;
}
.visit-steps li {
  display: flex;
  align-items: start;
  gap: 18px;
}
.visit-steps li > span {
  background: #deeee3;
  color: var(--pine);
  border-radius: 50%;
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  font-size: 14px;
  font-weight: 700;
}
.visit-steps h3 {
  font-size: 17px;
  font-weight: 650;
  margin: 3px 0 6px;
}
.visit-steps p {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.7;
  margin: 0;
}
.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 90px;
}
.contact-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
  margin: 0;
}
.contact-details dt {
  font-size: 14px;
  font-weight: 650;
  margin-bottom: 8px;
}
.contact-details dd {
  font-size: 14px;
  color: var(--muted);
  line-height: 1.8;
  margin: 0;
  white-space: pre-line;
  overflow-wrap: anywhere;
}
.contact-details a {
  color: var(--pine);
  text-decoration: underline;
  text-underline-offset: 4px;
}
.home-footer {
  background: var(--pine);
  color: white;
  padding-block: 30px;
}
.footer-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 22px;
}
.footer-brand {
  font-size: 22px;
  font-weight: 650;
}
.home-footer p {
  font-size: 13px;
  margin: 0;
  color: #d1e3d9;
}
.home-footer small {
  color: #d1e3d9;
  font-size: 12px;
}
@media (max-width: 800px) {
  .home-container {
    width: calc(100% - 40px);
  }
  .home-nav {
    gap: 18px;
  }
  .hero-grid {
    gap: 10px;
    padding-block: 48px;
  }
  .hero-description {
    font-size: 16px;
  }
  .section-heading {
    align-items: start;
    flex-direction: column;
  }
  .visit-grid,
  .contact-grid {
    gap: 40px;
  }
  .contact-details {
    grid-template-columns: 1fr;
  }
  .care-strip {
    gap: 12px;
  }
}
@media (max-width: 580px) {
  .header-inner {
    min-height: 82px;
    gap: 12px;
  }
  .brand {
    font-size: 22px;
    gap: 8px;
  }
  .brand img {
    width: 35px;
    height: 35px;
  }
  .brand small {
    font-size: 10px;
  }
  .home-nav .section-link {
    display: none;
  }
  .button-small {
    font-size: 13px;
    padding-inline: 14px;
  }
  .hero-grid,
  .visit-grid,
  .contact-grid {
    grid-template-columns: 1fr;
  }
  .hero-grid {
    gap: 25px;
    padding-block: 38px 28px;
  }
  .hero-art img {
    max-height: 270px;
  }
  .hero-description {
    max-width: 100%;
  }
  .hero-actions {
    gap: 20px;
  }
  .care-strip {
    grid-template-columns: 1fr;
    gap: 24px;
    padding-block: 27px;
  }
  .home-section {
    padding-block: 48px;
  }
  .service-list {
    grid-template-columns: 1fr;
  }
  .visit-section {
    padding-block: 44px;
  }
  .contact-details {
    grid-template-columns: 1fr 1fr;
  }
  .footer-inner {
    flex-direction: column;
    align-items: start;
    gap: 12px;
  }
}
@media (prefers-reduced-motion: no-preference) {
  .home-button,
  .text-link {
    transition:
      background-color 0.15s,
      color 0.15s;
  }
}
</style>
