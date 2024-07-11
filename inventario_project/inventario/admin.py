from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.core.cache import cache
from .models import MarcaRepuesto, MarcaMoto, UnidadMedida, Pais, Modelo, Repuesto, RepuestoModelo, Proveedor, RepuestoProxy
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def exportar_repuestos_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="repuestos.pdf"'
    
    p = canvas.Canvas(response, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Títulos
    p.setFont("Helvetica-Bold", 12)
    p.drawString(30, height - 40, "Lista de Repuestos")

    # Columnas
    p.setFont("Helvetica-Bold", 10)
    p.drawString(30, height - 60, "Código")
    p.drawString(100, height - 60, "Número de Parte")
    p.drawString(200, height - 60, "Nombre")
    p.drawString(350, height - 60, "Marca")
    p.drawString(450, height - 60, "UM")
    p.drawString(500, height - 60, "Procedencia")
    p.drawString(600, height - 60, "Precio Venta")

    # Datos
    y = height - 80
    p.setFont("Helvetica", 6)
    alternate = True
    for repuesto in queryset:
        if alternate:
            p.setFillColor(colors.whitesmoke)
        else:
            p.setFillColor(colors.lightgrey)
        p.rect(25, y - 10, width - 50, 20, fill=True, stroke=False)
        p.setFillColor(colors.black)
        
        p.drawString(30, y, str(repuesto.codigo))
        p.drawString(100, y, repuesto.numero_parte)
        p.drawString(200, y, repuesto.nombre)
        p.drawString(350, y, repuesto.marca_repuesto.nombre)
        p.drawString(450, y, repuesto.unidad_medida.descripcion)
        p.drawString(500, y, repuesto.pais.fabricacion)
        p.drawString(600, y, f"{repuesto.precio_venta:.2f}")
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 6)
        alternate = not alternate

    p.save()
    return response

exportar_repuestos_pdf.short_description = "Exportar seleccionados a PDF"

class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'numero_parte', 'nombre', 'cantidad', 'costo', 'precio_lista', 'precio_venta', 'get_marca', 'get_um', 'get_procedencia', 'get_modelos_compatibles', 'get_proveedor')
    search_fields = ('nombre', 'codigo', 'numero_parte', 'modelos__nombre')
    ordering = ('nombre',)

    def get_queryset(self, request):
        queryset = cache.get('repuesto_queryset')
        if not queryset:
            queryset = super().get_queryset(request).select_related('marca_repuesto', 'unidad_medida', 'pais', 'proveedor').prefetch_related('modelos')
            cache.set('repuesto_queryset', queryset, 60*15)  # Cache por 15 minutos
        return queryset

    def get_marca(self, obj):
        return obj.marca_repuesto.nombre
    get_marca.short_description = 'Marca'
    get_marca.admin_order_field = 'marca_repuesto__nombre'

    def get_um(self, obj):
        return obj.unidad_medida.descripcion
    get_um.short_description = 'UM'
    get_um.admin_order_field = 'unidad_medida__descripcion'

    def get_procedencia(self, obj):
        return obj.pais.fabricacion
    get_procedencia.short_description = 'Procedencia'
    get_procedencia.admin_order_field = 'pais__fabricacion'

    def get_modelos_compatibles(self, obj):
        return ", ".join([modelo.nombre for modelo in obj.modelos.all()])
    get_modelos_compatibles.short_description = 'Modelos Compatibles'

    def get_foto(self, obj):
        if obj.foto_url:
            return format_html(
                '<a href="#" onclick="openModal(\'{}\'); return false;">'
                '<img src="{}" style="width: 50px; height: 50px;" /></a>'
                '<div id="myModal" class="modal">'
                '<span class="close" onclick="closeModal()">&times;</span>'
                '<img class="modal-content" id="img01">'
                '<div id="caption"></div>'
                '</div>',
                obj.foto_url, obj.foto_url
            )
        return "No Image"
    get_foto.short_description = 'Foto'

    def get_proveedor(self, obj):
        return obj.proveedor.nombre if obj.proveedor else "No Proveedor"
    get_proveedor.short_description = 'Proveedor'
    get_proveedor.admin_order_field = 'proveedor__nombre'

    class Media:
        js = ('admin/js/custom_admin.js',)
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

class RepuestoSimpleAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'numero_parte', 'nombre', 'get_marca', 'get_um', 'get_procedencia', 'get_modelos_compatibles', 'precio_venta')
    search_fields = ('nombre', 'codigo', 'numero_parte', 'modelos__nombre')
    ordering = ('nombre',)
    actions = [exportar_repuestos_pdf]

    def get_queryset(self, request):
        queryset = cache.get('repuesto_simple_queryset')
        if not queryset:
            queryset = super().get_queryset(request).select_related('marca_repuesto', 'unidad_medida', 'pais').prefetch_related('modelos')
            cache.set('repuesto_simple_queryset', queryset, 60*15)  # Cache por 15 minutos
        return queryset

    def get_marca(self, obj):
        return obj.marca_repuesto.nombre
    get_marca.short_description = 'Marca'
    get_marca.admin_order_field = 'marca_repuesto__nombre'

    def get_um(self, obj):
        return obj.unidad_medida.descripcion
    get_um.short_description = 'UM'
    get_um.admin_order_field = 'unidad_medida__descripcion'

    def get_procedencia(self, obj):
        return obj.pais.fabricacion
    get_procedencia.short_description = 'Procedencia'
    get_procedencia.admin_order_field = 'pais__fabricacion'

    def get_modelos_compatibles(self, obj):
        return ", ".join([modelo.nombre for modelo in obj.modelos.all()])
    get_modelos_compatibles.short_description = 'Modelos Compatibles'

class RepuestoModeloAdmin(admin.ModelAdmin):
    list_display = ('get_repuesto', 'get_codigo', 'get_numero_parte', 'get_modelo', 'get_marca_repuesto', 'get_unidad_medida', 'get_pais_fabricacion')
    search_fields = ('repuesto__nombre', 'repuesto__codigo', 'repuesto__numero_parte', 'modelo__nombre')
    list_filter = ('repuesto__marca_repuesto', 'repuesto__unidad_medida', 'repuesto__pais')
    list_per_page = 25  # Pagina los resultados

    def get_queryset(self, request):
        queryset = cache.get('repuestomodelo_queryset')
        if not queryset:
            queryset = super().get_queryset(request).select_related('repuesto', 'repuesto__marca_repuesto', 'repuesto__unidad_medida', 'repuesto__pais', 'modelo')
            cache.set('repuestomodelo_queryset', queryset, 60*15)  # Cache por 15 minutos
        return queryset

    def get_repuesto(self, obj):
        return obj.repuesto.nombre
    get_repuesto.short_description = 'Repuesto'

    def get_codigo(self, obj):
        return obj.repuesto.codigo
    get_codigo.short_description = 'Código'

    def get_numero_parte(self, obj):
        return obj.repuesto.numero_parte
    get_numero_parte.short_description = 'Número de Parte'

    def get_modelo(self, obj):
        return obj.modelo.nombre
    get_modelo.short_description = 'Modelo'

    def get_marca_repuesto(self, obj):
        return obj.repuesto.marca_repuesto.nombre
    get_marca_repuesto.short_description = 'Marca del Repuesto'

    def get_unidad_medida(self, obj):
        return obj.repuesto.unidad_medida.descripcion
    get_unidad_medida.short_description = 'Unidad de Medida'

    def get_pais_fabricacion(self, obj):
        return obj.repuesto.pais.fabricacion
    get_pais_fabricacion.short_description = 'Procedencia'

admin.site.register(MarcaRepuesto)
admin.site.register(MarcaMoto)
admin.site.register(UnidadMedida)
admin.site.register(Pais)
admin.site.register(Modelo)
admin.site.register(Repuesto, RepuestoAdmin)
admin.site.register(RepuestoModelo, RepuestoModeloAdmin)
admin.site.register(Proveedor)
admin.site.register(RepuestoProxy, RepuestoSimpleAdmin)
