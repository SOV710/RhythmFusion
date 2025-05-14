<template>
  <el-main
    class="m-0 p-0 bg-gradient-to-b dark:from-[#212121] dark:to-[#121212] min-h-screen from-[#f2f2f2] to-[#e5e5e5]"
  >
    <div class="container mx-auto p-4">
      <el-form
        :model="form"
        ref="formRef"
        label-width="120px"
        class="max-w-md mx-auto bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg"
      >
        <h2 class="text-2xl font-bold mb-6 text-center dark:text-white">个人资料</h2>

        <!-- 头像上传 -->
        <el-form-item label="头像">
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
            <img v-if="form.avatar" :src="form.avatar" class="avatar" />
            <el-icon v-else class="avatar-placeholder">
              <Plus />
            </el-icon>
          </el-upload>
        </el-form-item>

        <!-- 用户名输入 -->
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>

        <!-- 姓名 -->
        <el-form-item label="姓名" prop="first_name">
          <div class="flex gap-2">
            <el-input v-model="form.first_name" placeholder="名" />
            <el-input v-model="form.last_name" placeholder="姓" />
          </div>
        </el-form-item>

        <!-- 邮箱 -->
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>

        <!-- 个人简介 -->
        <el-form-item label="个人简介" prop="bio">
          <el-input
            v-model="form.bio"
            type="textarea"
            :rows="3"
            placeholder="请输入个人简介"
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
            style="width: 100%"
          />
        </el-form-item>

        <!-- 保存按钮 -->
        <el-form-item>
          <el-button type="primary" @click="saveProfile" :loading="loading" class="w-full">
            保存
          </el-button>
        </el-form-item>
      </el-form>
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
  avatar: ''
})
const loading = ref(false)

// 为头像上传提供认证头信息
const uploadHeaders = computed(() => {
  return {
    Authorization: `Bearer ${userStore.accessToken}`
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
