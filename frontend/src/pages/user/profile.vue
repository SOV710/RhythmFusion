<template>
  <el-main
    class="m-0 p-0 bg-gradient-to-b dark:from-[#212121] dark:to-[#121212] min-h-screen from-[#f2f2f2] to-[#e5e5e5]"
  >
    <div class="container mx-auto p-4">
      <el-form
        :model="form"
        ref="formRef"
        label-width="100px"
        class="max-w-md mx-auto bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg"
      >
        <!-- 头像上传 -->
        <el-form-item label="Avatar">
          <el-upload
            class="avatar-uploader"
            action="/api/upload-avatar"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :on-success="handleAvatarSuccess"
            accept="image/*"
          >
            <img
              v-if="form.avatarUrl"
              :src="form.avatarUrl"
              class="avatar"
            />
            <i v-else class="el-icon-plus avatar-placeholder"></i>
          </el-upload>
        </el-form-item>

        <!-- 用户名输入 -->
        <el-form-item label="Username" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>

        <!-- 保存按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            @click="saveProfile"
            :loading="loading"
            class="w-full"
          >
            保存
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from '@/utils/axios'

interface ProfileForm {
  username: string
  avatarUrl: string
}

const formRef = ref()
const form = ref<ProfileForm>({ username: '', avatarUrl: '' })
const loading = ref(false)

// 上传前校验
function beforeAvatarUpload(file: File) {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isImage) {
    ElMessage.error('上传头像只能是图片格式!')
  }
  if (!isLt2M) {
    ElMessage.error('上传头像大小不能超过 2MB!')
  }
  return isImage && isLt2M
}

// 上传成功回调
function handleAvatarSuccess(response: any) {
  // 假设 response 返回 { url: string }
  form.value.avatarUrl = response.url
}

// 保存资料
async function saveProfile() {
  loading.value = true
  try {
    await axios.post('/api/profile', {
      username: form.value.username,
      avatar: form.value.avatarUrl,
    })
    ElMessage.success('保存成功')
  } catch (err) {
    ElMessage.error('保存失败')
  } finally {
    loading.value = false
  }
}

// 初始化获取用户信息
onMounted(async () => {
  try {
    const { data } = await axios.get('/api/profile')
    form.value.username = data.username
    form.value.avatarUrl = data.avatar
  } catch (err) {
    console.error(err)
  }
})
</script>

<style scoped lang="scss">
.avatar-uploader {
  display: block;
  text-align: center;
  .avatar-placeholder {
    font-size: 28px;
    color: #8c939d;
    width: 100px;
    height: 100px;
    line-height: 100px;
    border: 2px dashed #d9d9d9;
    border-radius: 50%;
    display: inline-block;
  }

  .avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    display: inline-block;
  }
}
</style>
