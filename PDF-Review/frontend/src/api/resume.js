import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    const message = error.response?.data?.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

export default {
  // 上传简历
  uploadResume(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/resume/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 提取信息
  extractInfo(resumeId) {
    return api.post('/resume/extract', { resume_id: resumeId })
  },

  // 匹配评分
  matchResume(resumeId, jobDescription) {
    return api.post('/resume/match', {
      resume_id: resumeId,
      job_description: jobDescription
    })
  },

  // 获取简历详情
  getResume(resumeId) {
    return api.get(`/resume/${resumeId}`)
  }
}
