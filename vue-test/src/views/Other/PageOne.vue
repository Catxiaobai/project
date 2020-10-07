<template>
  <div id="sample">
    <el-card>
      <!--      <el-button type="primary" @click="save">save</el-button>-->
      <!--      <el-button type="primary" @click="load">load</el-button>-->
      <span style="font-size: x-large;margin-left: 45%">完整性验证</span>
      <div id="myDiagramDiv" style="background-color: whitesmoke; border: solid 1px black; width: 60%; height: 480px;margin-top: 20px;margin-left: 20%"></div>
      <textarea id="myTransaction" style="width:100%;height:200px" v-show="false"></textarea>
      <textarea id="mytest" v-model="msg" v-show="false" />
      <el-button type="primary" style="margin-left: 45%;margin-top: 10px">完整性验证</el-button>
    </el-card>
  </div>
</template>

<script>
import go from 'gojs'
const MAKE = go.GraphObject.make
export default {
  name: 'PageThree.vue',
  data() {
    return {
      nodeDataArray: [],
      linkDataArray: [],
      text_data: {
        // class: 'go.GraphLinksModel',
        nodeKeyProperty: 'id',
        linkKeyProperty: 'id',
        nodeDataArray: [],
        linkDataArray: []
      },
      msg: 'result',
      test: 'tets'
      // myDiagram: ''
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    showIncremental(str) {
      // show the last transaction as an incremental update in JSON-formatted text
      var element = document.getElementById('myTransaction')
      // don't show anything upon the initial layout
      if (element.value === 'InitialLayout') str = ''
      element.value = str
    },
    save() {
      // document.getElementById('mySavedModel').value = this.myDiagram.model.toJson()
      console.log(this.myDiagram.model.toJson())
      this.postData(this.myDiagram.model.toJson())
      this.text_data = this.myDiagram.model.toJson()
      this.myDiagram.isModified = false
      this.showIncremental('')
    },
    load() {
      // var model = go.Model.fromJson(document.getElementById('mySavedModel').value)
      // establish GraphLinksModel functions:
      // node data id's are odd numbers
      var model = go.Model.fromJson(this.text_data)
      // console.log(this.text_data)
      // console.log(model.nodeDataArray)
      // console.log(document.getElementById('mySavedModel').value)
      model.makeUniqueKeyFunction = function(model, data) {
        var i = model.nodeDataArray.length * 2 + 1
        while (model.findNodeDataForKey(i) !== null) i += 2
        data.id = i // assume Model.nodeKeyProperty === "id"
        return i
      }
      // link data id's are even numbers
      model.makeUniqueLinkKeyFunction = function(model, data) {
        var i = model.linkDataArray.length * 2 + 2
        while (model.findLinkDataForKey(i) !== null) i += 2
        data.id = i // assume GraphLinksModel.linkKeyProperty === "id"
        return i
      }
      this.myDiagram.model = model
      this.showIncremental('')
    },
    getData() {
      this.$http
        .get('http://127.0.0.1:8000/api/deliver_model')
        .then(response => {
          console.log(response.data)
          this.linkDataArray = response.data.data_edge
          this.nodeDataArray = response.data.data_node
          this.text_data.nodeDataArray = this.nodeDataArray
          this.text_data.linkDataArray = this.linkDataArray
          // console.log(this.text_data)
          this.load()
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    postData: function(data) {
      this.$http
        .post('http://127.0.0.1:8000/api/verify_action', { add: data })
        .then(response => {
          console.log(response.data)
          if (response.data.error_code === 0) {
            this.$message({
              type: 'success',
              message: response.data.result
            })
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    init() {
      var element = document.getElementById('mytest')
      var $ = go.GraphObject.make
      this.myDiagram = $(go.Diagram, 'myDiagramDiv', {
        // have mouse wheel events zoom in and out instead of scroll up and down
        'toolManager.mouseWheelBehavior': go.ToolManager.WheelZoom,
        // support double-click in background creating a new node
        'clickCreatingTool.archetypeNodeData': { text: 'new node' },
        isReadOnly: true,
        // enable undo & redo
        'undoManager.isEnabled': false,
        layout: $(go.ForceDirectedLayout, {
          defaultSpringLength: 200,
          defaultElectricalCharge: 50,
          randomNumberGenerator: null,
          infinityDistance: 100
        })
      })
      // function ttt(e) {
      //   var element2 = document.getElementById('myTransaction')
      //   // don't show anything upon the initial layout
      //   // if (element2.value === 'InitialLayout') str = ''
      //   element2.value = e.model.toIncrementalJson(e)
      // }
      this.myDiagram.nodeTemplate = $(
        go.Node,
        'Auto',
        {
          cursor: 'pointer',
          // define a tooltip for each node that displays the color as text
          toolTip: $('ToolTip', $(go.TextBlock, { margin: 4 }, new go.Binding('text', 'name'))) // end of Adornment
        },
        new go.Binding('location', 'loc', go.Point.parse).makeTwoWay(go.Point.stringify),
        // define the node's outer shape, which will surround the TextBlock

        // 图标的style
        $(go.Shape, 'Circle', {
          desiredSize: new go.Size(60, 60),
          fill: $(go.Brush, 'Linear', { 0: 'rgb(0,191,255)', 1: 'rgb(30,144,255)' }),
          stroke: 'black',
          portId: '',
          fromLinkable: true,
          fromLinkableSelfNode: true,
          fromLinkableDuplicates: true,
          toLinkable: true,
          toLinkableSelfNode: true,
          toLinkableDuplicates: true,
          cursor: 'pointer'
        }),
        // 字体的style
        $(
          go.TextBlock,
          {
            font: 'bold 11pt helvetica, bold arial, sans-serif',
            editable: true // editing the text automatically updates the model data
          },
          new go.Binding('text', 'text').makeTwoWay()
        )
      )
      this.myDiagram.toolManager.hoverDelay = 10
      // //添加监听线生成事件
      // this.myDiagram.addDiagramListener('LinkDrawn', function(e) {
      //   console.log('线生成')
      //
      //   var data = { test: 'testjson' }
      //   postData(data)
      //   // this.postData({ test: 'tessss' })
      // })

      //添加监听线重新连接事件
      this.myDiagram.addDiagramListener('LinkRelinked', function(e) {
        console.log('线重连')
        var data = { test: 'testjson' }
        postData(data)
      })
      //添加监听线重新连接事件
      this.myDiagram.addDiagramListener('TextEdited', function(e) {
        console.log('文本编辑' + e)
      })
      // //添加修改事件
      // this.myDiagram.addDiagramListener('Modified', function(e) {
      //   console.log('修改' + e)
      // })
      // //添加监听节点生成事件
      // this.myDiagram.addDiagramListener('externalobjectsdropped', function(e) {
      //   e.subject.each(function(n) {
      //     console.log('节点生成')
      //   })
      // })
      //
      // this.myDiagram.addModelChangedListener(function(e) {
      //   if (e.isTransactionFinished) {
      //     console.log('剩下的' + e.model.toJson())
      //     var json = e.model.toIncrementalJson(e)
      //     console.log('修改的信息' + json)
      //     // record each Transaction as a JSON-format string
      //     // ... send to server/database ...
      //   }
      // })
      // 监听删除事件
      this.myDiagram.addDiagramListener('SelectionDeleted', function(e) {
        console.log(e)
        e.subject.each(function(n) {
          // console.log('delete:' + JSON.stringify(n.data))
          //
          // console.log('total:' + e.diagram.model.toJson())
          // 传递删除信息和剩下的信息
          var data = { total: e.diagram.model.toJson(), delete: JSON.stringify(n.data) }
          postData(data)
        })
      })
      // 监听添加事件
      this.myDiagram.addDiagramListener('LinkDrawn', function(e) {
        console.log('add:' + JSON.stringify(e.subject.data))
        console.log('total:' + e.diagram.model.toJson())
        // 传递添加的信息和剩下的信息
        var data = { total: e.diagram.model.toJson(), add: JSON.stringify(e.subject.data) }
        postData(data)
      })
      // 向后端传递变化信息
      function postData(data) {
        var httpRequest = new XMLHttpRequest() //第一步：创建需要的对象
        httpRequest.open('POST', 'http://127.0.0.1:8000/api/verify_action', true) //第二步：打开连接
        httpRequest.setRequestHeader('Content-type', 'application/json') //设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
        httpRequest.send(JSON.stringify(data)) //发送请求 将情头体写在send中
        /**
         * 获取数据后的处理程序
         */
        httpRequest.onreadystatechange = function() {
          //请求后的回调接口，可将请求成功后要执行的程序写在其中
          if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            //验证请求是否发送成功
            var json = JSON.parse(httpRequest.responseText) //获取到服务端返回的数据
            console.log(json)
            element.value = json['result']
          }
        }
      }
      function test(str) {
        console.log(element)
        element.value = str
        // console.log(element.value)
      }

      // unlike the normal selection Adornment, this one includes a Button
      this.myDiagram.nodeTemplate.selectionAdornmentTemplate = $(
        go.Adornment,
        'Spot',
        $(
          go.Panel,
          'Auto',
          $(go.Shape, { fill: null, stroke: 'blue', strokeWidth: 2 }),
          $(go.Placeholder) // this represents the selected Node
        ),
        // the button to create a "next" node, at the top-right corner
        $(
          'Button',
          {
            alignment: go.Spot.TopRight,
            click: addNodeAndLink // this function is defined below
          },
          $(go.Shape, 'PlusLine', { desiredSize: new go.Size(6, 6) })
        ) // end button
      ) // end Adornment
      // and adds a link to that new node
      function addNodeAndLink(e, obj) {
        var adorn = obj.part
        e.handled = true
        var diagram = adorn.diagram
        diagram.startTransaction('Add State')

        // get the node data for which the user clicked the button
        var fromNode = adorn.adornedPart
        var fromData = fromNode.data
        // create a new "State" data object, positioned off to the right of the adorned Node
        var toData = { text: 'new' }
        var p = fromNode.location.copy()
        p.x += 100
        toData.loc = go.Point.stringify(p) // the "loc" property is a string, not a Point object
        // add the new node data to the model
        var model = diagram.model
        model.addNodeData(toData)

        // create a link data from the old node data to the new node data
        var linkdata = {
          from: model.getKeyForNodeData(fromData), // or just: fromData.id
          to: model.getKeyForNodeData(toData),
          text: 'transition'
        }
        // and add the link data to the model
        model.addLinkData(linkdata)

        // select the new Node
        var newnode = diagram.findNodeForData(toData)
        diagram.select(newnode)

        diagram.commitTransaction('Add State')

        // if the new node is off-screen, scroll the diagram to show the new node
        diagram.scrollToRect(newnode.actualBounds)
      }

      // this.myDiagram.addDiagramListener('addNodeAndLink', function() {
      //   console.log('test')
      // })
      // replace the default Link template in the linkTemplateMap
      this.myDiagram.linkTemplate = $(
        go.Link, // the whole link panel
        {
          curve: go.Link.Bezier,
          adjusting: go.Link.Stretch,
          reshapable: true,
          relinkableFrom: true,
          relinkableTo: true
        },
        {
          cursor: 'pointer',
          // define a tooltip for each node that displays the color as text
          toolTip: $('ToolTip', $(go.TextBlock, { margin: 4 }, new go.Binding('text', 'action'))) // end of Adornment
        },
        {
          click: function(e, obj) {
            console.log('e:' + e + '---obj:' + obj.part.data)
            console.log('Clicked on ' + obj.part.data.key)
          }
        },
        new go.Binding('points').makeTwoWay(),
        new go.Binding('curviness', 'curviness'),
        $(
          go.Shape, // the link shape
          { strokeWidth: 1.5 }
        ),
        $(
          go.Shape, // the arrowhead
          { toArrow: 'standard', stroke: null }
        ),
        $(
          go.Panel,
          'Auto',
          $(
            go.Shape, // the label background, which becomes transparent around the edges
            {
              fill: $(go.Brush, 'Radial', { 0: 'rgb(240, 240, 240)', 0.3: 'rgb(240, 240, 240)', 1: 'rgba(240, 240, 240, 0)' }),
              stroke: null
            }
          ),
          $(
            go.TextBlock,
            'transition', // the label text
            {
              textAlign: 'center',
              font: '10pt helvetica, arial, sans-serif',
              stroke: 'black',
              margin: 4,
              editable: true // editing the text automatically updates the model data
            },
            new go.Binding('text', 'text').makeTwoWay()
          )
        )
      )
      // // Show the diagram's model in JSON format
      // function save() {
      //   document.getElementById('mySavedModel').value = this.myDiagram.model.toJson()
      //   this.myDiagram.isModified = false
      //   showIncremental('')
      // }
      // function load() {
      //   var model = go.Model.fromJson(document.getElementById('mySavedModel').value)
      //   // establish GraphLinksModel functions:
      //   // node data id's are odd numbers
      //   model.makeUniqueKeyFunction = function(model, data) {
      //     var i = model.nodeDataArray.length * 2 + 1
      //     while (model.findNodeDataForKey(i) !== null) i += 2
      //     data.id = i // assume Model.nodeKeyProperty === "id"
      //     return i
      //   }
      //   // link data id's are even numbers
      //   model.makeUniqueLinkKeyFunction = function(model, data) {
      //     var i = model.linkDataArray.length * 2 + 2
      //     while (model.findLinkDataForKey(i) !== null) i += 2
      //     data.id = i // assume GraphLinksModel.linkKeyProperty === "id"
      //     return i
      //   }
      //   this.myDiagram.model = model
      //   showIncremental('')
      // }
      // function showIncremental(str) {
      //   // show the last transaction as an incremental update in JSON-formatted text
      //   var element = document.getElementById('myTransaction')
      //   // don't show anything upon the initial layout
      //   if (element.value === 'InitialLayout') str = ''
      //   element.value = str
      // }
      // this.load()
    }
  },
  created() {
    this.getData()
  }
  // watch: {
  //   msg(newVal, oldVal) {
  //     console.log('新值：' + newVal, '旧值：' + oldVal)
  //     console.log('msg:' + this.msg)
  //   }
  // }
  // computed: {
  //   // 计算属性的 getter
  //   reversedMessage: function() {
  //     // `this` 指向 vm 实例
  //     return this.msg
  //       .split('')
  //       .reverse()
  //       .join('')
  //   }
  // }
}
</script>

<style scoped></style>
