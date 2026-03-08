<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>🎯 智能简历分析系统</h1>
          <p>AI 赋能的简历解析与岗位匹配</p>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>
        <p>© 2026 智能简历分析系统 | Powered by AI</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.el-container {
  min-height: 100vh;
}

.el-header {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-content {
  text-align: center;
}

.header-content h1 {
  color: #667eea;
  font-size: 28px;
  margin-bottom: 5px;
}

.header-content p {
  color: #666;
  font-size: 14px;
}

.el-main {
  padding: 40px 20px;
}

.el-footer {
  background: rgba(255, 255, 255, 0.9);
  text-align: center;
  line-height: 60px;
  color: #666;
  font-size: 14px;
}
</style>
