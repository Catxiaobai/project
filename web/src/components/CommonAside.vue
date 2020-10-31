<template>
  <div id="common-aside">
    <div id="aside-content" style="height: 100%">
      <el-menu router :default-active="$route.path" style="height: 100%" :unique-opened="true">
        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-folder"></i>
            <span>软件安全性分析</span>
          </template>
          <el-submenu index="1-1">
            <template slot="title"><i class="el-icon-folder"></i>使用场景建模</template>
            <el-submenu index="1-1-1">
              <template slot="title"> <i class="el-icon-folder"></i>子使用场景建模</template>
              <el-menu-item index="/subSceneInfo"><i class="el-icon-folder"></i>子使用场景描述</el-menu-item>
              <el-menu-item index="/subSceneModel"><i class="el-icon-folder"></i>子使用场景构建</el-menu-item>
            </el-submenu>
            <el-submenu index="1-1-2">
              <template slot="title"><i class="el-icon-folder"></i>综合使用场景建模</template>
              <el-menu-item index="/complexSceneInfo"><i class="el-icon-folder"></i>综合使用场景描述</el-menu-item>
              <el-menu-item index="/complexSceneModel"><i class="el-icon-folder"></i>综合使用场景构建</el-menu-item>
            </el-submenu>
            <el-menu-item index="/listGeneration"><i class="el-icon-folder"></i>模型列表生成</el-menu-item>
          </el-submenu>
          <el-submenu index="1-2">
            <template slot="title"><i class="el-icon-folder"></i>分析规则设置</template>
            <el-menu-item index="/generalRules"><i class="el-icon-folder"></i>通用分析规则选择</el-menu-item>
            <el-menu-item index="/specialRules"><i class="el-icon-folder"></i>项目分析规则设置</el-menu-item>
            <el-menu-item index="/instantiate"><i class="el-icon-folder"></i>分析规则实例化</el-menu-item>
          </el-submenu>

          <el-submenu index="1-3">
            <template slot="title"><i class="el-icon-folder"></i>分析实施</template>
            <el-menu-item index="/check"><i class="el-icon-folder"></i>模型检验</el-menu-item>
            <el-menu-item index="/failureAnalysis"><i class="el-icon-folder"></i>失效分析</el-menu-item>
            <el-menu-item index="/demandExtraction"><i class="el-icon-folder"></i>软件安全性需求提取</el-menu-item>
          </el-submenu>

          <el-menu-item index="/requirements"><i class="el-icon-folder"></i>软件安全性需求管理</el-menu-item>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-folder"></i>
            <span>软件安全性设计</span>
          </template>
          <el-submenu index="2-1">
            <template slot="title"><i class="el-icon-folder"></i>设计准则设置</template>
            <el-menu-item index="/generalCriteria"><i class="el-icon-folder"></i>通用设计准则选择</el-menu-item>
            <el-menu-item index="/specialCriteria"><i class="el-icon-folder"></i>专用设计准则设置</el-menu-item>
          </el-submenu>
          <el-menu-item index="/verification"><i class="el-icon-folder"></i>核查实施</el-menu-item>
          <el-menu-item index="/complete"><i class="el-icon-folder"></i>设计完善</el-menu-item>
          <el-menu-item index="/designTable"><i class="el-icon-folder"></i>软件安全性设计管理</el-menu-item>
        </el-submenu>
      </el-menu>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommonAside.vue',
  data() {
    return {
      asideMenu: [],
      value: '',
      options: [
        {
          value: 'ss',
          label: 'ss'
        }
      ],
      itemInfo: 'test'
    }
  },
  methods: {
    clickMenu(item) {
      if (this.$route.name !== item.name) {
        this.$router.push({ name: item.name })
      }
      // this.$store.commit('selectMenu', item)
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log('item', this.itemInfo)
    }
  },
  mounted() {
    this.getItemInfo()
  },
  updated() {
    this.getItemInfo()
  },
  created() {
    this.getItemInfo()
  },
  computed: {}
}
</script>

<style scoped lang="scss">
#common-aside {
  background: lightyellow;
  width: 100%;
  height: 100%;
  font-weight: bold;
  //display: flex;
  #aside-content {
    width: 100%;
    height: 100%;
  }
}
</style>
