<template>
  <div id="common-aside">
    <div id="aside-content">
      <el-menu id="menu">
        <el-menu-item id="noChildren" :index="item.path" v-for="item in noChildren" :key="item.path" @click="clickMenu(item)">
          <i :class="'el-icon-' + item.icon"></i>
          <span slot="title">{{ item.label }}</span>
        </el-menu-item>
        <el-submenu id="hasChildren" :index="item.path" v-for="item in hasChildren" :key="item.path" @click="clickMenu(item)">
          <template slot="title" id="title">
            <i :class="'el-icon-' + item.icon"></i>
            <span class="name">{{ item.label }}</span>
          </template>
          <el-menu-item-group id="child">
            <el-menu-item :index="subItem.path" v-for="subItem in item.children" :key="subItem.path" @click="clickMenu(subItem)">
              <i :class="'el-icon-caret-right'"></i>
              <span class="name">{{ subItem.label }}</span>
            </el-menu-item>
          </el-menu-item-group>
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
          path: '/one',
          name: 'one',
          label: '子场景建模',
          icon: 's-claim',
          children: [
            {
              path: '/login',
              name: 'login',
              label: '功能模型导入'
            },
            {
              path: '/login',
              name: 'login',
              label: '场景要素建模'
            },
            {
              path: '/login',
              name: 'login',
              label: '要素列表生成'
            }
          ]
        },
        {
          path: '/two',
          name: 'two',
          label: '综合场景建模',
          icon: 's-claim',
          children: [
            {
              path: '/login',
              name: 'login',
              label: '外部交联环境建模'
            },
            {
              path: '/login',
              name: 'login',
              label: '功能处理建模'
            },
            {
              path: '/login',
              name: 'login',
              label: '功能层次建模'
            },
            {
              path: '/login',
              name: 'login',
              label: '状态迁移建模'
            }
          ]
        },
        {
          path: '/three',
          name: 'three',
          label: '安全性分析',
          icon: 's-claim',
          children: [
            {
              path: '/login',
              name: 'login',
              label: '分析规则管理'
            },
            {
              path: '/login',
              name: 'login',
              label: '分析实施'
            },
            {
              path: '/login',
              name: 'login',
              label: '软件安全性需求提取'
            }
          ]
        },
        {
          path: '/four',
          name: 'four',
          label: '安全性设计核查',
          icon: 's-claim',
          children: [
            {
              path: '/login',
              name: 'login',
              label: '设计准则管理'
            },
            {
              path: '/login',
              name: 'login',
              label: '设计核查实施'
            },
            {
              path: '/login',
              name: 'login',
              label: '设计完善措施'
            }
          ]
        },
        {
          path: '/five',
          name: 'five',
          label: '安全性数据库',
          icon: 's-claim',
          children: [
            {
              path: '/login',
              name: 'login',
              label: '软件失效数据管理'
            },
            {
              path: '/login',
              name: 'login',
              label: '系统危险数据管理'
            },
            {
              path: '/login',
              name: 'login',
              label: '安全性分析规则管理'
            },
            {
              path: '/login',
              name: 'login',
              label: '设计准则管理'
            }
          ]
        },
        {
          path: '/six',
          name: 'six',
          label: '分析报告生成',
          icon: 's-claim',
          children: [
            {
              path: '/login',
              name: 'login',
              label: '报告生成'
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
  },
  computed: {
    noChildren() {
      return this.asideMenu.filter(item => !item.children)
    },
    hasChildren() {
      return this.asideMenu.filter(item => item.children)
    }
  }
}
</script>

<style scoped lang="scss">
#common-aside {
  background: lightyellow;
  width: 100%;
  height: 600px;
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
        .name {
          font-size: 14px;
        }
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
