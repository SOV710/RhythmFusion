<template>
  <el-main
    class="main-gradient-bg m-0 p-0 bg-gradient-to-b dark:from-[#212121] dark:via-[#1a1a1a] dark:to-[#121212] from-[#f8f9fa] via-[#f0f2f5] to-[#e5e8ed] min-h-screen"
  >
    <div class="content-container">
      <div class="profile-card">
        <div class="page-header">
          <div class="title-icon">
            <i class="el-icon-user"></i>
          </div>
          <h1 class="page-title">个人资料</h1>
        </div>

        <!-- 头像上传 - 单独为头像创建一个区域 -->
        <div class="avatar-section">
          <el-upload
            class="avatar-uploader"
            :action="`/api/user/profile/`"
            :headers="uploadHeaders"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :on-success="handleAvatarSuccess"
            :on-error="handleUploadError"
            :http-request="customUpload"
            name="avatar"
            accept="image/*"
          >
            <div class="avatar-container">
              <img v-if="form.avatar" :src="form.avatar" class="avatar-image" />
              <div v-else class="avatar-placeholder">
                <i class="el-icon-plus"></i>
              </div>
              <div class="avatar-overlay">
                <i class="el-icon-camera"></i>
                <span>更换头像</span>
              </div>
            </div>
          </el-upload>
        </div>

        <el-form :model="form" ref="formRef" label-width="100px" class="profile-form">
          <!-- 用户名输入 -->
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              prefix-icon="el-icon-user"
            />
          </el-form-item>

          <!-- 姓名 -->
          <el-form-item label="姓名" prop="first_name">
            <div class="name-inputs">
              <el-input
                v-model="form.first_name"
                placeholder="名"
                prefix-icon="el-icon-user"
                class="firstname-input"
              />
              <el-input
                v-model="form.last_name"
                placeholder="姓"
                prefix-icon="el-icon-user"
                class="lastname-input"
              />
            </div>
          </el-form-item>

          <!-- 邮箱 -->
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="form.email" placeholder="请输入邮箱" prefix-icon="el-icon-message" />
          </el-form-item>

          <!-- 个人简介 -->
          <el-form-item label="个人简介" prop="bio">
            <el-input
              v-model="form.bio"
              type="textarea"
              :rows="4"
              placeholder="请输入个人简介"
              class="bio-input"
            />
          </el-form-item>

          <!-- 出生日期 -->
          <el-form-item label="出生日期" prop="birth_date">
            <el-date-picker
              v-model="form.birth_date"
              type="date"
              placeholder="选择日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              class="date-picker"
            />
          </el-form-item>

          <!-- 保存按钮 -->
          <el-form-item class="form-actions">
            <el-button
              type="primary"
              @click="saveProfile"
              :loading="loading"
              class="save-button animated-button"
            >
              <i class="el-icon-check mr-1"></i>
              保存个人资料
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </el-main>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import type { User } from '@/api/modules/user'
import type { UploadRequestOptions } from 'element-plus'

// 扩展User类型以包含上传文件
interface ProfileForm extends Partial<User> {
  avatarFile?: File
}

// 初始化用户store
const userStore = useUserStore()

// 表单引用和数据
const formRef = ref()
const form = ref<ProfileForm>({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  bio: '',
  birth_date: '',
  avatar: '',
})
const loading = ref(false)

// 为头像上传提供认证头信息
const uploadHeaders = computed(() => {
  return {
    Authorization: `Bearer ${userStore.accessToken}`,
  }
})

// 自定义上传方法，将头像作为表单一部分处理
function customUpload(options: UploadRequestOptions): Promise<any> {
  return new Promise((resolve) => {
    // 我们不在这里直接上传，而是存储文件引用以供保存时上传
    form.value.avatarFile = options.file

    // 创建本地预览
    const reader = new FileReader()
    reader.onload = (e) => {
      form.value.avatar = e.target?.result as string
      // 手动调用成功回调，以更新UI
      options.onSuccess?.('')
      resolve('')
    }
    reader.readAsDataURL(options.file)
  })
}

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
function handleAvatarSuccess() {
  ElMessage.success('头像已准备就绪，点击保存生效')
}

// 上传失败回调
function handleUploadError(error: any) {
  console.error('头像上传失败:', error)
  ElMessage.error('头像上传失败，请重试')
}

// 保存资料
async function saveProfile() {
  loading.value = true
  try {
    // 将表单数据转为FormData，以支持文件上传
    const formData = new FormData()

    // 只添加已修改的字段
    Object.entries(form.value).forEach(([key, value]) => {
      if (value !== null && value !== undefined && key !== 'avatarFile') {
        formData.append(key, value as string)
      }
    })

    // 特殊处理头像文件
    if (form.value.avatarFile) {
      formData.append('avatar', form.value.avatarFile)
    }

    // 调用pinia store方法更新资料
    await userStore.updateProfile(formData)
    ElMessage.success('个人资料保存成功')

    // 清除临时文件引用
    form.value.avatarFile = undefined
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请重试')
  } finally {
    loading.value = false
  }
}

// 初始化获取用户信息
onMounted(async () => {
  try {
    await userStore.fetchProfile()
    // 填充表单数据
    if (userStore.profile) {
      form.value = { ...userStore.profile }
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error('获取用户信息失败')
  }
})
</script>

<style scoped lang="scss">
@import '@/styles/components/base.scss';

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;

  @include mobile {
    padding: 1rem;
  }
}

.profile-card {
  @include rf-card;
  padding: 2rem;
  max-width: 700px;
  margin: 0 auto;
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);

  @media (prefers-color-scheme: dark) {
    background-color: rgba(30, 30, 30, 0.8);
  }

  @include mobile {
    padding: 1.5rem;
  }
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;

  .title-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--rf-primary), var(--rf-secondary));
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
    box-shadow: var(--rf-shadow-md);
  }

  .page-title {
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0;
    @include rf-text-gradient;
  }
}

.avatar-section {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;

  .avatar-uploader {
    .avatar-container {
      position: relative;
      width: 140px;
      height: 140px;
      border-radius: 50%;
      overflow: hidden;
      cursor: pointer;
      box-shadow: var(--rf-shadow-md);
      border: 3px solid rgba(var(--rf-primary-rgb), 0.3);
      transition: all var(--rf-transition-normal);

      &:hover {
        border-color: var(--rf-primary);
        transform: scale(1.05);

        .avatar-overlay {
          opacity: 1;
        }
      }

      .avatar-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }

      .avatar-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: rgba(var(--rf-primary-rgb), 0.1);
        font-size: 2rem;
        color: var(--rf-primary);
      }

      .avatar-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        opacity: 0;
        transition: opacity var(--rf-transition-normal);

        i {
          font-size: 1.5rem;
          margin-bottom: 0.5rem;
        }

        span {
          font-size: 0.9rem;
        }
      }
    }
  }
}

.profile-form {
  .name-inputs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;

    @include mobile {
      grid-template-columns: 1fr;
    }
  }

  :deep(.el-input__wrapper) {
    box-shadow: var(--rf-shadow-sm);
    transition: all var(--rf-transition-normal);
    border-radius: 8px;

    &:focus-within {
      box-shadow: 0 0 0 1px var(--rf-primary) !important;
      transform: translateY(-2px);
    }
  }

  .bio-input {
    :deep(.el-textarea__inner) {
      border-radius: 8px;
      resize: none;

      &:focus {
        box-shadow: 0 0 0 1px var(--rf-primary) !important;
      }
    }
  }

  .date-picker {
    width: 100%;
  }

  .form-actions {
    margin-top: 2rem;
    display: flex;
    justify-content: center;
  }

  .save-button {
    padding: 0.75rem 2rem;
    font-weight: 500;
    width: 100%;
    max-width: 300px;
    background: linear-gradient(90deg, var(--rf-primary), var(--rf-secondary));
    border: none;

    &:hover {
      transform: translateY(-3px);
      box-shadow: var(--rf-shadow-md);
    }
  }
}

// Responsive adjustments
@media (max-width: 640px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;

    .title-icon {
      width: 40px;
      height: 40px;
      font-size: 1.25rem;
    }

    .page-title {
      font-size: 1.5rem;
    }
  }

  .profile-form {
    :deep(.el-form-item__label) {
      float: none;
      display: block;
      text-align: left;
      padding: 0 0 8px;
      line-height: 1.5;
    }

    :deep(.el-form-item__content) {
      margin-left: 0 !important;
    }
  }
}
</style>
