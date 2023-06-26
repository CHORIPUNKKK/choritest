function eliminarPerfil() {
  Swal.fire({
    title: 'Confirmar',
    text: '¿Desea eliminar su perfil?',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: 'Perfil eliminado',
        text: 'Su perfil ha sido eliminado exitosamente',
        icon: 'success'
      }).then(function() {
        window.location.href = "/eliminar-perfil/";
      });
    }
  });
}
function eliminarProducto(id) {
    Swal.fire({
      title: 'Confirmar',
      text: '¿Desea Eliminar?',
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'success'
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire('Eliminado!','Producto Eliminado Correctamente','success').then(function() {
            window.location.href = "/delate/"+id+"/";
        })
      }
    })
}

function eliminarCarrito(id) {
  Swal.fire({
    title: 'Confirmar',
    text: '¿Desea Eliminar?',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'success'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire('Eliminado!','Producto Quitado Del Carrito','success').then(function() {
          window.location.href = "/eliminar/"+id+"/";
      })
    }
  })
}

function eliminarCupones(id) {
  Swal.fire({
    title: 'Confirmar',
    text: '¿Desea Eliminar?',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'success'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire('Eliminado!','Producto Eliminado Correctamente','success').then(function() {
          window.location.href = "/elimina_cup/"+id+"/";
      })
    }
  })
}