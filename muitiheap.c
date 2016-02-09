#include "Python.h"

static void down(PyObject *heap, int len, int i){
    int min;
    while(i*2<=len){
        if(i*2+1 > len)
            min = i * 2;
        else{
            if(PyInt_AS_LONG(PyList_GetItem(PyList_GetItem(heap,i*2-1),0)) < PyInt_AS_LONG(PyList_GetItem(PyList_GetItem(heap,i*2),0)))
                min = i * 2;
            else
                min = i * 2 + 1;
        }
        if(PyInt_AS_LONG(PyList_GetItem(PyList_GetItem(heap,i-1),0))>PyInt_AS_LONG(PyList_GetItem(PyList_GetItem(heap,min-1),0))){
            PyObject *a,*b;
            a = PyList_GetItem(heap,i-1);
            b = PyList_GetItem(heap,min-1);
            Py_XINCREF(a);Py_XINCREF(b);
            PyList_SetItem(heap,i-1,b);
            PyList_SetItem(heap,min-1,a);    
        }
        i = min;
    }
}

static void heapify(PyObject *heap, int len){
    long i = len/2 + 1;
    while(i>0){
        down(heap,len,i);
        i--;
    }
}

static void replace(PyObject *heap, int len, int i,int j){
    PyList_SetItem(PyList_GetItem(heap,0),0,PyInt_FromLong(i));
    PyList_SetItem(PyList_GetItem(heap,0),1,PyInt_FromLong(j));
    down(heap,len,1);
}

static PyObject *
he_getcandidates(PyObject *self, PyObject *args)
{
    PyObject *list,*entity_len,*inlist_len,*inindex,*inlist,*result,*tokens;
    int len,loe,los,e,ei,pi;
    float T;
    float threshold = 0.8;
    result = PyList_New(0);
    if (!PyArg_ParseTuple(args, "O!lO!O!O!O!O!", &PyList_Type,&list,&los,&PyDict_Type,&entity_len,&PyDict_Type,&inlist_len,&PyList_Type,&inindex,&PyDict_Type,&inlist,&PyList_Type,&tokens))
        return NULL; 
    int *current_index=(int*)malloc(sizeof(int)*los);
    for(int i=0;i<los;i++){
        current_index[i] = 0;
    }
    len = PyList_GET_SIZE(list);
    heapify(list,len);
    int occur = 0;
    e = PyInt_AS_LONG(PyList_GetItem(PyList_GetItem(list,0),0));
    while(1){
        ei = PyInt_AS_LONG(PyList_GetItem(PyList_GetItem(list,0),0));
        pi = PyInt_AS_LONG(PyList_GetItem(PyList_GetItem(list,0),1));
        if(ei == 237392 || pi == -1)
            break;
        if(ei == e)
            occur++;
        else{
            loe = PyInt_AS_LONG(PyDict_GetItem(entity_len,PyList_GetItem(inindex,e)));
            T = floor((loe+los)*(threshold/(1+threshold)));
            if (occur >= T)
                PyList_Append(result,PyList_GetItem(inindex,e));
            e = ei;
            occur = 1;
        }
        if (PyInt_AS_LONG(PyDict_GetItem(inlist_len,PyList_GetItem(tokens,pi))) > current_index[pi]+1){
            current_index[pi]++;
            replace(list,len,PyInt_AS_LONG(PyList_GetItem(PyDict_GetItem(inlist,PyList_GetItem(tokens,pi)),current_index[pi])),pi);
        }
        else
            replace(list,len,237392,-1);
    }
    Py_XINCREF(result);
    return result;
}
 
static PyMethodDef faerie_methods[] = {
    {"getcandidates", he_getcandidates, METH_VARARGS, "return candidates"},
    {NULL, NULL}
};
 
PyMODINIT_FUNC
initfaerie(void)
{
    Py_InitModule("faerie", faerie_methods);
}