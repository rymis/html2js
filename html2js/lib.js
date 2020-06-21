// html2js support library

"use strict";

var h2j = {
};

// Application base class. This class contains methods for mounting elements, running application, etc.
h2j.Application = function () {
    this.data = {};
};

h2j.Application.prototype = {
    // Mount application to some element. This element will be used for rendering.
    // Function could mount application to some DOM Element or select element using querySelector function.
    "mount": function (selectorOrElement) {
    },

    // Render mounted application. Could be used to manually re-render everything.
    "render": function () {
    }
};

// List represents list of items. Every item in this list will be wrapped into Namespace object.
h2j.List = function () {
    this._data = [];
};

h2j.List.prototype = {
    // Push element to the end of the list
    "push": function (item) {
    },

    // Remove the last element
    "pop": function () {
    },

    // Add item to the beginning of the list
    "unshift": function (item) {
    },

    // Remove item from the beginning of the list
    "shift": function () {
    },

    // Replace elements in the list
    "splice": function (start) {

    },

    "removeAt": function (index) {

    },

    // Renders list into DOM element
    "render": function (index) {
    }
};

