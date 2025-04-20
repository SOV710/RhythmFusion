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
    class="m-0 p-0 bg-gradient-to-b dark:from-[#212121] dark:to-[#121212] min-h-screen from-[#f2f2f2] to-[#e5e5e5]"
  >
    <el-menu
      class="m-0 flex flex-wrap items-center justify-left text-left"
      style="background-color: rgba(255, 255, 255, 0)"
      :ellipsis="false"
      router
    >
      <el-menu-item index="/" class="p-0 m-0">
        <el-button round size="large"> Home </el-button>
      </el-menu-item>
      <el-menu-item index="/music/" class="p-0 m-0">
        <el-button round size="large"> Music </el-button>
      </el-menu-item>
    </el-menu>

    <h1 color="$el-color-primary" class="text-4xl">
      {{ msg }}
    </h1>

    <p class="text-lg p-4">
      This is a website build with
      <a href="https://vuejs.org/" target="_blank"> Vue 3</a> +
      <a href="https://vite.dev/" target="_blank"> Vite</a> +
      <a href="https://www.typescriptlang.org/" target="_blank"> Typescript</a> +
      <a href="https://sass-lang.com/" target="_blank"> Sass/SCSS</a> +
      <a href="https://router.vuejs.org/" target="_blank"> Vue-Router</a> +
      <a href="https://pinia.vuejs.org/" target="_blank"> Pinia</a> +
      <a href="https://element-plus.org/" target="_blank"> Element Plus</a>, and
      <a href="https://unocss.dev/" target="_blank"> Unocss</a>
    </p>

    <div class="glow-container" @mousemove="handleMouseMove">
      <div class="glow-layer" :style="glowStyle"></div>
      <img
        src="@/assets/logo.png"
        alt="Logo"
        class="p-10 glow-image"
        style="width: 500px; height: auto; filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.8))"
      />
    </div>
  </el-main>
</template>

<style lang="scss" scoped>
.glow-container {
  position: relative;
  display: inline-block;
  overflow: visible;
}

/* 图片样式 */
.glow-image {
  display: block;
  position: relative;
  z-index: 2;
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

  /* 初始背景为蓝色 */
  background: rgba(0, 0, 255, 0.5);
  filter: blur(100px);

  /* 动画实现彩虹渐变效果 */
  animation: glowRainbow 10s ease-in-out infinite alternate;
}

/* 定义动画 keyframes */
@keyframes glowRainbow {
  0% {
    background: rgba(0, 0, 255, 0.5); // 蓝色
    filter: blur(101px);
  }
  20% {
    background: rgba(75, 0, 130, 0.5); // 靛蓝
    filter: blur(102px);
  }
  40% {
    background: rgba(238, 130, 238, 0.5); // 紫罗兰
    filter: blur(103px);
  }
  60% {
    background: rgba(0, 255, 0, 0.5); // 绿色
    filter: blur(104px);
  }
  80% {
    background: rgba(255, 255, 0, 0.5); // 黄色
    filter: blur(105px);
  }
  100% {
    background: rgba(255, 0, 0, 0.5); // 红色
    filter: blur(106px);
  }
}
</style>
