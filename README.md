HTML2JS
------------------
Convert HTML templates to fast JavaScript code. This compiler creates
bidirectional bindings and allows to use simple methods for data modifications.
Every modification is immediately applied in DOM with minimal number of
operations. The idea comes from Svetle framework but this script is
lightweight, which means you can easyly modify it and add your functionality.

Example
============
Let's try to build simple TODO application:
``` html
<html>
    <head>
        <title>TODO</title>
    </head>
    <body>
        <!-- Here we will place rendered application. Model name is a name of global variable containing model. -->
        <render name="app" data="data">
            <ul>
            <!-- for iterates over the model field. Collection will be created implicitly for this field. -->
                <for var="todo" in="data.todo">
                    <!-- You can use standard javascript constructions in templates -->
                    <li class="{{todo.done?'done':'waiting'}}">
                        <!-- This text will be taken from todo.text element -->
                        {{todo.text}}
                        <button onclick="removeItem({{todo.elementIndex()}})" value="X">
                        <button onclick="toggleDone({{todo.elementIndex()}})" value="V">
                    </li>
                </for>
            </ul>
            <!-- Here I use square braces which means I want to create bidirectional binding -->
            <input type="text" value="[[todo.newItem]]"><button value="Add" onclick="addItem()">
        </render>

        <script>
var data = app();

function removeItem(idx) {
    data.todo.removeItem(idx);
}

function toggleDone(idx) {
    data.todo[idx].done = !data.todo[idx].done;
}

function addItem() {
    data.todo.push({"text": data.newItem, "done": false});
}
        </script>

    </body>
</html>
```
