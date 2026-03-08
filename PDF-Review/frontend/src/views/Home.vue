<template>
  <div class="home">
    <el-row :gutter="20">
      <!-- 左侧：上传和信息展示 -->
      <el-col :xs="24" :sm="24" :md="12">
        <el-card class="upload-card">
          <template #header>
            <div class="card-header">
              <el-icon><Upload /></el-icon>
              <span>简历上传</span>
            </div>
          </template>
          
          <el-upload
            class="upload-dragger"
            drag
            :auto-upload="false"
            :on-change="handleFileChange"
            :limit="1"
            accept=".pdf"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              拖拽 PDF 文件到此处或 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                仅支持 PDF 格式，文件大小不超过 10MB
              </div>
            </template>
          </el-upload>

          <el-button 
            type="primary" 
            :loading="uploading"
            :disabled="!selectedFile"
            @click="uploadResume"
            style="width: 100%; margin-top: 20px;"
          >
            {{ uploading ? '上传中...' : '开始解析' }}
          </el-button>
        </el-card>

        <!-- 提取的信息 -->
        <el-card v-if="extractedInfo" class="info-card" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <el-icon><User /></el-icon>
              <span>简历信息</span>
            </div>
          </template>

          <el-descriptions :column="1" border>
            <el-descriptions-item label="姓名">
              {{ extractedInfo.basic_info?.name || '未识别' }}
            </el-descriptions-item>
            <el-descriptions-item label="电话">
              {{ extractedInfo.basic_info?.phone || '未识别' }}
            </el-descriptions-item>
            <el-descriptions-item label="邮箱">
              {{ extractedInfo.basic_info?.email || '未识别' }}
            </el-descriptions-item>
            <el-descriptions-item label="地址">
              {{ extractedInfo.basic_info?.address || '未识别' }}
            </el-descriptions-item>
            <el-descriptions-item label="求职意向">
              {{ extractedInfo.job_intention?.position || '未识别' }}
            </el-descriptions-item>
            <el-descriptions-item label="期望薪资">
              {{ extractedInfo.job_intention?.salary || '未识别' }}
            </el-descriptions-item>
            <el-descriptions-item label="工作年限">
              {{ extractedInfo.background?.work_years || 0 }} 年
            </el-descriptions-item>
            <el-descriptions-item label="学历">
              {{ extractedInfo.background?.education || '未识别' }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <!-- 右侧：岗位匹配 -->
      <el-col :xs="24" :sm="24" :md="12">
        <el-card class="match-card">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>岗位匹配</span>
            </div>
          </template>

          <el-input
            v-model="jobDescription"
            type="textarea"
            :rows="8"
            placeholder="请输入岗位描述，例如：&#10;&#10;招聘 Python 后端工程师&#10;要求：&#10;- 3 年以上 Python 开发经验&#10;- 熟悉 Django/Flask 框架&#10;- 熟悉 MySQL、Redis&#10;- 有微服务架构经验优先"
            :disabled="!currentResumeId"
          />

          <el-button
            type="success"
            :loading="matching"
            :disabled="!currentResumeId || !jobDescription"
            @click="matchResume"
            style="width: 100%; margin-top: 20px;"
          >
            {{ matching ? '匹配中...' : '开始匹配' }}
          </el-button>
        </el-card>

        <!-- 匹配结果 -->
        <el-card v-if="matchResult" class="result-card" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <el-icon><TrendCharts /></el-icon>
              <span>匹配结果</span>
            </div>
          </template>

          <div class="score-display">
            <el-progress
              type="circle"
              :percentage="matchResult.match_score"
              :color="getScoreColor(matchResult.match_score)"
              :width="150"
            >
              <template #default="{ percentage }">
                <span class="score-text">{{ percentage }}</span>
                <span class="score-label">分</span>
              </template>
            </el-progress>
          </div>

          <el-divider />

          <div class="detail-scores">
            <div class="score-item">
              <span>技能匹配</span>
              <el-progress
                :percentage="matchResult.details?.skill_match || 0"
                :color="getScoreColor(matchResult.details?.skill_match)"
              />
            </div>
            <div class="score-item">
              <span>经验匹配</span>
              <el-progress
                :percentage="matchResult.details?.experience_match || 0"
                :color="getScoreColor(matchResult.details?.experience_match)"
              />
            </div>
            <div class="score-item">
              <span>学历匹配</span>
              <el-progress
                :percentage="matchResult.details?.education_match || 0"
                :color="getScoreColor(matchResult.details?.education_match)"
              />
            </div>
          </div>

          <el-divider />

          <div v-if="matchResult.matched_keywords?.length" class="keywords">
            <h4>匹配关键词</h4>
            <el-tag
              v-for="keyword in matchResult.matched_keywords"
              :key="keyword"
              type="success"
              style="margin: 5px;"
            >
              {{ keyword }}
            </el-tag>
          </div>

          <el-alert
            :title="matchResult.suggestions"
            :type="getSuggestionType(matchResult.match_score)"
            :closable="false"
            style="margin-top: 15px;"
          />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload, UploadFilled, User, Document, TrendCharts } from '@element-plus/icons-vue'
import resumeApi from '../api/resume'

export default {
  name: 'Home',
  components: {
    Upload,
    UploadFilled,
    User,
    Document,
    TrendCharts
  },
  setup() {
    const selectedFile = ref(null)
    const uploading = ref(false)
    const matching = ref(false)
    const currentResumeId = ref('')
    const extractedInfo = ref(null)
    const jobDescription = ref('')
    const matchResult = ref(null)

    const handleFileChange = (file) => {
      if (file.raw.type !== 'application/pdf') {
        ElMessage.error('只支持 PDF 格式')
        return
      }
      if (file.raw.size > 10 * 1024 * 1024) {
        ElMessage.error('文件大小不能超过 10MB')
        return
      }
      selectedFile.value = file.raw
    }

    const uploadResume = async () => {
      if (!selectedFile.value) {
        ElMessage.warning('请先选择文件')
        return
      }

      uploading.value = true
      try {
        // 上传文件
        const uploadRes = await resumeApi.uploadResume(selectedFile.value)
        if (uploadRes.code === 200) {
          currentResumeId.value = uploadRes.data.resume_id
          ElMessage.success('上传成功，正在提取信息...')

          // 提取信息
          const extractRes = await resumeApi.extractInfo(currentResumeId.value)
          if (extractRes.code === 200) {
            extractedInfo.value = extractRes.data
            ElMessage.success('信息提取完成')
          }
        }
      } catch (error) {
        ElMessage.error(error.message || '操作失败')
      } finally {
        uploading.value = false
      }
    }

    const matchResume = async () => {
      if (!currentResumeId.value || !jobDescription.value) {
        ElMessage.warning('请先上传简历并输入岗位描述')
        return
      }

      matching.value = true
      try {
        const res = await resumeApi.matchResume(currentResumeId.value, jobDescription.value)
        if (res.code === 200) {
          matchResult.value = res.data
          ElMessage.success('匹配完成')
        }
      } catch (error) {
        ElMessage.error(error.message || '匹配失败')
      } finally {
        matching.value = false
      }
    }

    const getScoreColor = (score) => {
      if (score >= 80) return '#67c23a'
      if (score >= 60) return '#e6a23c'
      return '#f56c6c'
    }

    const getSuggestionType = (score) => {
      if (score >= 80) return 'success'
      if (score >= 60) return 'warning'
      return 'info'
    }

    return {
      selectedFile,
      uploading,
      matching,
      currentResumeId,
      extractedInfo,
      jobDescription,
      matchResult,
      handleFileChange,
      uploadResume,
      matchResume,
      getScoreColor,
      getSuggestionType
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 1400px;
  margin: 0 auto;
}

.upload-card,
.info-card,
.match-card,
.result-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.upload-dragger {
  width: 100%;
}

.score-display {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.score-text {
  font-size: 32px;
  font-weight: bold;
  color: #333;
}

.score-label {
  font-size: 14px;
  color: #666;
  margin-left: 5px;
}

.detail-scores {
  padding: 10px 0;
}

.score-item {
  margin-bottom: 15px;
}

.score-item span {
  display: block;
  margin-bottom: 8px;
  color: #666;
  font-size: 14px;
}

.keywords h4 {
  margin-bottom: 10px;
  color: #333;
  font-size: 16px;
}

@media (max-width: 768px) {
  .el-col {
    margin-bottom: 20px;
  }
}
</style>
