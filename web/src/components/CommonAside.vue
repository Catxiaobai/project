<template>
  <div id="common-aside">
    <div id="aside-content" style="height: 100%">
      <el-menu router :default-active="$route.path" class="el-menu-vertical-demo" style="height: 100%">
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
        </el-submenu>
      </el-menu>
    </div>
    <div id="aside-right"></div>
  </div>
</template>

<script>
export default {
  name: 'CommonAside.vue',
  data() {
    return {
      asideMenu: [
        {
          path: '/item',
          name: 'item',
          label: '项目管理',
          icon: 's-claim'
        },
        {
          path: '/infoManage/system1',
          name: 'system',
          label: '软件安全性分析',
          icon: 's-claim',
          children: [
            {
              path: '/personnel',
              name: 'personnel',
              label: '使用场景建模'
            },
            {
              path: '/authority',
              name: 'authority',
              label: '分析规则设置'
            },
            {
              path: '/tools',
              name: 'tools',
              label: '分析实施'
            },
            {
              path: '/tools',
              name: 'tools',
              label: '软件安全性需求管理'
            }
          ]
        },
        {
          path: '/infoManage/system',
          name: 'system',
          label: '软件安全性设计',
          icon: 's-claim',
          children: [
            {
              path: '/personnel',
              name: 'personnel',
              label: '设计准则设置',
              children: [
                {
                  path: '/personnel',
                  name: 'personnel',
                  label: '通用设计准则选择'
                },
                {
                  path: '/authority',
                  name: 'authority',
                  label: '项目设计准则库'
                }
              ]
            },
            {
              path: '/authority',
              name: 'authority',
              label: '核查实施'
            },
            {
              path: '/tools',
              name: 'tools',
              label: '设计完善'
            }
          ]
        }
      ]
    }
  },
  methods: {
    clickMenu(item) {
      if (this.$route.name !== item.name) {
        this.$router.push({ name: item.name })
      }
      // this.$store.commit('selectMenu', item)
    }
  },
  computed: {
    noChildren() {
      return this.asideMenu.filter(item => !item.children)
    },
    hasChildren() {
      // console.log(
      //   'hasChildren',
      //   this.asideMenu.filter(item => item.children)
      // )
      return this.asideMenu.filter(item => item.children)
    },
    hasChildren2(data) {
      data = this.asideMenu
      return data.filter(item => item.children)
    }
  }
}
</script>

<style scoped lang="scss">
#common-aside {
  background: lightyellow;
  width: 100%;
  height: 100%;
  font-weight: bold;
  display: flex;
  #aside-content {
    width: 100%;
    height: 100%;
    #menu {
      height: 100%;
      //background: skyblue;
      #noChildren {
        //background: yellow;
        font-size: 18px;
      }
      #hasChildren {
        //background: moccasin;
        #child {
          background: whitesmoke;
        }
      }
      .name {
        font-size: 14px;
      }
    }
  }
  #aside-right {
    background: skyblue;
    width: 5px;
    height: 100%;
  }
}
</style>
