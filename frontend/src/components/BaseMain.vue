<script setup lang="ts">
defineProps<{ msg: string }>()

const glowOffset = reactive({ x: 0, y: 0 })
const glowStyle = computed(() => {
  return {
    transform: `translate(${glowOffset.x}px, ${glowOffset.y}px)`,
  }
})

function handleMouseMove(event: MouseEvent) {
  // 获取 glow-container 元素的位置和尺寸
  const container = document.querySelector('.glow-container') as HTMLElement
  if (!container) return
  const rect = container.getBoundingClientRect()
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  // 计算鼠标相对于 glow-container 中心的偏移
  const offsetX = (event.clientX - rect.left - centerX) * 0.05
  const offsetY = (event.clientY - rect.top - centerY) * 0.05
  glowOffset.x = offsetX
  glowOffset.y = offsetY
}

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
})

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', handleMouseMove)
})
</script>

<template>
  <el-main
    class="base-layout-main main-gradient-bg m-0 p-0 dark:from-[#212121] dark:via-[#1a1a1a] dark:to-[#121212] from-[#f8f9fa] via-[#f0f2f5] to-[#e5e8ed] min-h-screen bg-gradient-to-b"
  >
    <div class="content-container">
      <div class="navigation-menu">
        <el-button
          type="primary"
          class="nav-button animated-button"
          round
          @click="$router.push('/')"
        >
          Home
        </el-button>
        <el-button
          type="primary"
          class="nav-button animated-button"
          round
          @click="$router.push('/music/')"
        >
          Music
        </el-button>
      </div>

      <h1 class="welcome-heading text-4xl md:text-5xl font-bold mb-8">
        {{ msg }}
      </h1>

      <p class="welcome-description text-lg leading-relaxed mb-10 max-w-3xl mx-auto">
        Experience music like never before with
        <a href="https://vuejs.org/" target="_blank" class="tech-link"> Vue 3</a> +
        <a href="https://vite.dev/" target="_blank" class="tech-link"> Vite</a> +
        <a href="https://www.typescriptlang.org/" target="_blank" class="tech-link"> TypeScript</a> +
        <a href="https://sass-lang.com/" target="_blank" class="tech-link"> SCSS</a> +
        <a href="https://router.vuejs.org/" target="_blank" class="tech-link"> Vue-Router</a> +
        <a href="https://pinia.vuejs.org/" target="_blank" class="tech-link"> Pinia</a> +
        <a href="https://element-plus.org/" target="_blank" class="tech-link"> Element Plus</a>, and
        <a href="https://unocss.dev/" target="_blank" class="tech-link"> UnoCSS</a>
      </p>

      <div class="glow-container" @mousemove="handleMouseMove">
        <div class="glow-layer" :style="glowStyle"></div>
        <img
          src="@/assets/logo.png"
          alt="Rhythm Fusion Logo"
          class="logo-image"
        />
      </div>

      <div class="features-section">
        <div class="feature-card hover-card">
          <div class="feature-icon">
            <i class="el-icon-headset"></i>
          </div>
          <h3>Discover Music</h3>
          <p>Find new artists and songs tailored to your taste</p>
        </div>
        
        <div class="feature-card hover-card">
          <div class="feature-icon">
            <i class="el-icon-star-on"></i>
          </div>
          <h3>Create Playlists</h3>
          <p>Curate your perfect music collections</p>
        </div>
        
        <div class="feature-card hover-card">
          <div class="feature-icon">
            <i class="el-icon-connection"></i>
          </div>
          <h3>Share & Connect</h3>
          <p>Connect with friends and share your favorite tunes</p>
        </div>
      </div>
    </div>
  </el-main>
</template>

<style lang="scss" scoped>
@import '@/styles/components/base.scss';

.navigation-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  
  .nav-button {
    font-weight: 500;
    padding: 0.5rem 1.25rem;
    border: none;
    background: linear-gradient(90deg, var(--rf-primary) 0%, var(--rf-secondary) 100%);
    box-shadow: 0 4px 15px rgba(var(--rf-primary-rgb), 0.3);
    color: white;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-3px);
      box-shadow: 0 6px 20px rgba(var(--rf-primary-rgb), 0.4);
    }
    
    &:active {
      transform: translateY(-1px);
    }
  }
}

.welcome-heading {
  text-align: center;
  @include rf-text-gradient;
  margin-bottom: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.welcome-description {
  text-align: center;
  color: var(--rf-text-secondary-light);
  max-width: 700px;
  margin: 0 auto 3rem;
  line-height: 1.6;
  
  @media (prefers-color-scheme: dark) {
    color: var(--rf-text-secondary-dark);
  }
  
  .tech-link {
    position: relative;
    color: var(--rf-primary);
    font-weight: 500;
    text-decoration: none;
    transition: all 0.2s;
    padding: 0 0.15rem;
    
    &::after {
      content: '';
      position: absolute;
      width: 100%;
      height: 2px;
      bottom: -2px;
      left: 0;
      background: linear-gradient(90deg, var(--rf-primary), var(--rf-secondary));
      transform: scaleX(0);
      transform-origin: center;
      transition: transform 0.3s ease;
    }
    
    &:hover {
      color: var(--rf-primary-dark);
      
      &::after {
        transform: scaleX(1);
      }
    }
  }
}

.glow-container {
  position: relative;
  display: flex;
  justify-content: center;
  overflow: visible;
  margin: 2rem auto;
  width: 500px;
  max-width: 100%;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    transform: scale(1.2);
    z-index: 0;
  }
}

.logo-image {
  width: 100%;
  height: auto;
  filter: drop-shadow(0 10px 25px rgba(var(--rf-primary-rgb), 0.5));
  position: relative;
  z-index: 2;
  animation: floatAnimation 6s ease-in-out infinite;
}

/* 光晕层 */
.glow-layer {
  position: absolute;
  top: 10%;
  left: 10%;
  width: 80%;
  height: 80%;
  transform: translate(-50%, -50%);
  z-index: 1;
  pointer-events: none;
  background: rgba(var(--rf-primary-rgb), 0.5);
  filter: blur(100px);
  animation: glowRainbow 10s ease-in-out infinite alternate;
}

/* 定义动画 keyframes */
@keyframes glowRainbow {
  0% {
    background: rgba(74, 134, 232, 0.5); // 主色蓝
    filter: blur(101px);
  }
  20% {
    background: rgba(108, 45, 199, 0.5); // 次色紫
    filter: blur(102px);
  }
  40% {
    background: rgba(238, 130, 238, 0.5); // 紫罗兰
    filter: blur(103px);
  }
  60% {
    background: rgba(0, 200, 83, 0.5); // 绿色
    filter: blur(104px);
  }
  80% {
    background: rgba(255, 193, 7, 0.5); // 黄色
    filter: blur(105px);
  }
  100% {
    background: rgba(233, 30, 99, 0.5); // 粉色
    filter: blur(106px);
  }
}

@keyframes floatAnimation {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-15px);
  }
}

.features-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 4rem;
  
  .feature-card {
    @include rf-card;
    padding: 2rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: var(--rf-border-radius-lg);
    
    @media (prefers-color-scheme: dark) {
      background-color: rgba(30, 30, 30, 0.7);
      backdrop-filter: blur(10px);
    }
    
    .feature-icon {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--rf-primary-light), var(--rf-secondary));
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 1.5rem;
      color: white;
      font-size: 1.5rem;
      box-shadow: 0 8px 20px rgba(var(--rf-primary-rgb), 0.3);
    }
    
    h3 {
      font-size: 1.25rem;
      font-weight: 600;
      margin-bottom: 0.75rem;
      color: var(--rf-text-primary-light);
      
      @media (prefers-color-scheme: dark) {
        color: var(--rf-text-primary-dark);
      }
    }
    
    p {
      color: var(--rf-text-secondary-light);
      line-height: 1.5;
      
      @media (prefers-color-scheme: dark) {
        color: var(--rf-text-secondary-dark);
      }
    }
  }
}

// Responsive adjustments
@media (max-width: 768px) {
  .logo-image {
    width: 90%;
  }
  
  .features-section {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>
