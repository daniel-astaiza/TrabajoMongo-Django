function eliminarPelicula(id){
    Swal.fire({
        title: 'Estas seguro de eliminar la Película',
        showDenyButton: true,
        confirmButtonText: 'SI',
        denyButtonText: 'NO',
        icon: 'question'
    }).then((result) => {
        if (result.isConfirmed){
            location.href="/eliminarPelicula/"+id
        }
    });
}
