<template>
  <el-menu>
    <el-submenu :index="item.path" v-for="item in hasChildren" :key="item.path" class="el-parent-menu">
      <template slot="title">
        <i :class="'el-icon-' + item.icon"></i>
        <span style="font-size: 18px;font-weight: bold">{{ item.label }}</span>
      </template>
      <el-menu-item-group class="el-children-menu">
        <el-menu-item :index="subItem.path" v-for="subItem in item.children" :key="subItem.path" @click="clickMenu(subItem)">
          {{ subItem.label }}
        </el-menu-item>
      </el-menu-item-group>
    </el-submenu>
  </el-menu>
</template>

<script>
export default {
  name: 'InnerAside.vue',
  computed: {
    noChildren() {
      return this.asideMenu.filter(item => !item.children)
    },
    hasChildren() {
      return this.asideMenu.filter(item => item.children)
    },
    isCollape() {
      return this.$store.state.tab.isCollapsed
    }
  },
  data() {
    return {
      asideMenu: [
        {
          path: '/used',
          label: '使用场景维护',
          name: 'used',
          icon: 's-claim',
          index: 1,
          children: [
            {
              path: '/usedTrace',
              label: '场景查看2.0',
              name: 'usedTrace'
            },
            {
              path: '/used',
              label: '场景查看',
              name: 'used'
            },
            {
              path: '/importTrace',
              label: '场景导入',
              name: 'importTrace'
            },
            {
              path: '/addTrace',
              label: '场景添加',
              name: 'addTrace'
            }
          ]
        },
        {
          path: '/model',
          label: '模型构建',
          name: 'model',
          icon: 'magic-stick',
          index: 3,
          children: [
            {
              path: '/createModel',
              label: '模型生成',
              name: 'createModel'
            },
            {
              path: '/showModel',
              label: '模型查看',
              name: 'showModel'
            }
          ]
        },
        {
          path: '/verify',
          label: '模型验证',
          icon: 's-cooperation',
          index: 4,
          children: [
            {
              path: '/judgeModel',
              label: '完整性验证',
              name: 'judgeModel',
              icon: 's-help'
            },
            {
              path: '/completionModel',
              label: '模型补全',
              name: 'completionModel',
              icon: 'more'
            }
          ]
        },
        {
          path: '/invalid',
          label: '失效场景维护',
          name: 'invalid',
          icon: 's-release',
          index: 2,
          children: [
            {
              path: '/invalid',
              label: '场景查看',
              name: 'invalid'
            },
            {
              path: '/importInvalidTrace',
              label: '场景导入',
              name: 'importInvalidTrace'
            },
            {
              path: '/addInvalidTrace',
              label: '场景添加',
              name: 'addInvalidTrace'
            }
          ]
        },
        {
          path: '/analyze',
          label: '安全性分析',
          icon: 's-platform',
          index: 5,
          children: [
            {
              path: '/invalidVerify',
              label: '安全性验证2.0',
              name: 'invalidVerify',
              icon: 'more'
            },
            {
              path: '/safeVerify',
              label: '安全性验证',
              name: 'safeVerify',
              icon: 'more'
            },
            {
              path: '/safeAssess',
              label: '安全性评估',
              name: 'safeAssess',
              icon: 'more'
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
      this.$store.commit('selectMenu', item)
    }
  }
}
</script>

<style lang="scss" scoped>
.el-menu {
  height: 100%;
}
.el-menu-item {
  font-size: 16px;
}
.el-parent-menu {
  //background-color: #deebf7;
}
.el-children-menu {
  background-color: whitesmoke;
}
</style>

<style lang="scss">
//设置了默认左边框为白色
.el-submenu .el-submenu__title.active {
  border-left: #fff solid 6px;
}
//设置鼠标悬停时el-submenu的样式
.el-submenu .el-submenu__title:hover {
  border-left: #33a2ef solid 6px !important;
  background-color: #e2eff9 !important;
  color: #38b2ff !important;
  i {
    color: #38b2ff;
  }
}
</style>

<style lang="scss">
//设置了默认左边框为白色
.el-menu-item {
  border-left: #fff solid 6px;
}

//设置鼠标悬停时el-menu-item的样式
.el-menu-item:hover {
  border-left: #33a2ef solid 6px !important;
  background-color: #e2eff9 !important;
  color: #38b2ff !important;
  //less语法，实现鼠标悬停时icon变色
  i {
    color: #38b2ff;
  }
}
.el-menu-item.is-active {
  border-left: #33a2ef solid 6px !important;
  background-color: #e2eff9 !important;
  color: #38b2ff !important;
  //less语法，实现鼠标悬停时icon变色
  i {
    color: #38b2ff;
  }
}
</style>
