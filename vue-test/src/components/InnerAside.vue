<template>
  <el-menu :collapse="isCollape" default-active="2" class="el-menu-vertical-demo" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
    <el-menu-item :index="item.path" v-for="item in noChildren" :key="item.path" @click="clickMenu(item)" style="font-size: large">
      <i :class="'el-icon-' + item.icon"></i>
      <span slot="title">{{ item.label }}</span>
    </el-menu-item>
    <el-submenu :index="item.path" v-for="item in hasChildren" :key="item.path">
      <template slot="title">
        <i :class="'el-icon-' + item.icon"></i>
        <span>{{ item.label }}</span>
      </template>
      <el-menu-item-group>
        <el-menu-item :index="subItem.value" v-for="(subItem, subIndex) in item.children" :key="subIndex" @click="clickMenu(subItem)">{{
          subItem.label
        }}</el-menu-item>
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
          label: '使用场景',
          name: 'used',
          icon: 's-claim',
          index: 1,
          children: [
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
          path: '/invalid',
          label: '失效场景',
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
            // {
            //   path: '/editModel',
            //   label: '模型编辑',
            //   name: 'editModel'
            // }

            // {
            //   path: '/safety',
            //   label: '安全性评估',
            //   name: 'safety',
            //   icon: 'warning'
            // }
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
          path: '/analyze',
          label: '安全性分析',
          icon: 's-platform',
          index: 5,
          children: [
            {
              path: '/safeVerify',
              label: '安全性验证',
              name: 'safeVerify',
              icon: 'more'
            },
            {
              path: '/safeAssess',
              label: '安全性评估',
              name: 'page2',
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
        // this.$router.replace(item.path)
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
</style>
