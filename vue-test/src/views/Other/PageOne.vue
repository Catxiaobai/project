<template>
  <el-card class="box-card">
    <!--    <el-button type="primary" @click="changeStatus">back</el-button>-->
    <iframe id="iframeContain" name="iframeContain" seamless scrolling="yes" src="http://127.0.0.1:8000/api/test" v-if="true">
      您当前的浏览器不支持页面上的功能，请升级您当前的浏览器版本或使用谷歌浏览器访问当前页面
    </iframe>
  </el-card>
</template>

<script>
export default {
  name: 'PageOne.vue',
  data() {
    return {
      cardMainShow: true,
      cardHtmlShow: false
      //   isChange: false
    }
  },
  methods: {
    changeStatus() {
      // if (this.isChange) {
      this.cardMainShow = !this.cardMainShow
      this.cardHtmlShow = !this.cardHtmlShow
      // }
    }
  }
}
</script>

<style lang="scss" scoped>
/** iframe样式 */
#iframeContain {
  width: 100%;
  height: 600px;
}
</style>
