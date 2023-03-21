#include <Python.h>
#include <stdlib.h>

static PyObject* generate_random_number(PyObject* self, PyObject* args) {
    int n;
    if (!PyArg_ParseTuple(args, "i", &n)) {
        return NULL;
    }
    return PyLong_FromLong(rand() % n);
}

static PyMethodDef my_module_ext_methods[] = {
    {"generate_random_number", generate_random_number, METH_VARARGS, "Generate a random number"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef my_module_ext_module = {
    PyModuleDef_HEAD_INIT,
    "cextension",
    "Odoo CPython extension module",
    -1,
    my_module_ext_methods
};

PyMODINIT_FUNC PyInit_my_module_ext(void) {
    return PyModule_Create(&my_module_ext_module);
}