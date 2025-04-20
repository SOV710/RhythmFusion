<script setup lang="ts">
import { ElMessage } from 'element-plus'


import blues from '@/assets/bg/blues.jpg'
import classical from '@/assets/bg/classical.png'
import country from '@/assets/bg/country.png'
import dance from '@/assets/bg/dance.png'
import electronic from '@/assets/bg/electronic.png'
import folk from '@/assets/bg/folk.png'
import hiphop from '@/assets/bg/hiphop.png'
import jazz from '@/assets/bg/jazz.png'
import jpop from '@/assets/bg/jpop.jpg'
import metal from '@/assets/bg/metal.png'
import pop from '@/assets/bg/pop.png'
import punk from '@/assets/bg/punk.png'
import rab from '@/assets/bg/rab.png'
import rock from '@/assets/bg/rock.png'

const genres = ref([
  { name: 'Blues', image: blues, artists: 'B.B. King, Muddy Waters, Eric Clapton' },
  { name: 'Classical', image: classical, artists: 'Ludwig van Beethoven, Wolfgang Amadeus Mozart, Johann Sebastian Bach' },
  { name: 'Country', image: country, artists: 'Johnny Cash, Dolly Parton, Willie Nelson' },
  { name: 'Dance', image: dance, artists: 'Daft Punk, Calvin Harris, Avicii' },
  { name: 'Electronic', image: electronic, artists: 'Kraftwerk, Skrillex, Deadmau5' },
  { name: 'Folk', image: folk, artists: 'Bob Dylan, Joan Baez, Simon & Garfunkel' },
  { name: 'HipHop', image: hiphop, artists: 'Kendrick Lamar, Eminem, Jay-Z' },
  { name: 'Jazz', image: jazz, artists: 'Miles Davis, John Coltrane, Louis Armstrong' },
  { name: 'J-Pop', image: jpop, artists: 'n-buna, Utada Hikaru, Kenshi Yonezu, YOASOBI' },
  { name: 'Metal', image: metal, artists: 'Metallica, Iron Maiden, Black Sabbath' },
  { name: 'Pop', image: pop, artists: 'Michael Jackson, Taylor Swift, Madonna' },
  { name: 'Punk', image: punk, artists: 'The Clash, Ramones, Sex Pistols' },
  { name: 'R&B', image: rab, artists: 'Beyoncé, Usher, Alicia Keys' },
  { name: 'Rock', image: rock, artists: 'Queen, The Beatles, Led Zeppelin' },
])

function selectGenre(name: string) {
  ElMessage.success(`Do you want to generate suggested playlist in ${name}?`)
}
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

    <div
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6 custom-container"
    >
      <el-card
        v-for="(g) in genres"
        :key="g.name"
        class="genre-card"
        :style="{ '--bg-image': `url(${g.image})` }"
        @click="() => selectGenre(g.name)"
      >
          <div class="card-header">
            <span class="text-4xl">{{ g.name }}</span>
          <p>{{ g.artists }} and more</p>
          </div>
      </el-card>

    </div>
  </el-main>
</template>

<style scoped lang="scss">
.custom-container {
  > * {
    max-width: 480px;
    min-height: 600px;
  }
}

.custom-card {
  cursor: pointer;
  background-size: cover;
  background-position: center;
  /* remove default padding in el-card */
  .el-card__body { padding: 0; }
}

.genre-card {
  position: relative;
  overflow: hidden;
  cursor: pointer;

  /* 背景图和基础样式 */
  background-image: var(--bg-image);
  background-size: cover;
  background-position: center;
  height: 200px;
  display: flex;
  flex-direction: column;
  text-align: left;

  /* 上半部分深色渐变：从上到中间 */
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0; right: 0;
    height: 50%;
    background: linear-gradient(
      to bottom,
      rgba(0, 0, 0, 0.8),
      transparent
    );
    pointer-events: none;
    z-index: 1;
  }

  /* 下半部分深色渐变：从下到中间 */
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0; right: 0;
    height: 50%;
    background: linear-gradient(
      to top,
      rgba(0, 0, 0, 0.8),
      transparent
    );
    pointer-events: none;
    z-index: 1;
  }

  /* 确保 header 和 body 在蒙版之上 */
  :deep(.el-card__header),
  :deep(.el-card__body) {
    position: relative;
    z-index: 2;
    background: transparent !important;
  }
}
</style>
