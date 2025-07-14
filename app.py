import  streamlit as st
import pandas as pd
import  numpy as np

st.title("Canadá Xpress")

file = st.file_uploader("Sube tu archivo de ventas de SICAR", type="xlsx")
st.html(
    """    
    <style>
        [data-testid='stFileUploaderDropzoneInstructions'] > div > span {
            display: none;
        }

        [data-testid='stFileUploaderDropzoneInstructions'] > div::before {
            content: 'Arrastre aquí los archivos';
        }

        [data-testid='stBaseButton-secondary'] {
            text-indent: -9999px;
            line-height: 0;
        }

        [data-testid='stBaseButton-secondary']::after {
            line-height: initial;
            content: "Buscar";
            text-indent: 0;
        }

        [data-testid='stFileUploaderDropzoneInstructions'] > div > small {
            display: none;
        }

        [data-testid='stFileUploaderDropzoneInstructions'] > div::after {
            content: 'Límite 200MB por archivo';
            display: block;
        }     
        [data-testid='stMainBlockContainer'] {
            padding-top: 50px;
        }
        
    </style>
    """
)


if file is not None:
    archivoSICAR = pd.read_excel(file, header = 5)
    archivoSICAR = archivoSICAR[["Unnamed: 1", "Unnamed: 4", "Fecha", "Usuario"]]
    # Renombrar columnas correctamente
    archivoSICAR = archivoSICAR.rename(columns={
        "Unnamed: 1": "Total_Registrado",
        "Unnamed: 4": "Producto",
    })

    # Llenar filas vacias con el valor anterior
    archivoSICAR['Fecha'] = archivoSICAR['Fecha'].ffill()
    archivoSICAR['Usuario'] = archivoSICAR['Usuario'].ffill()

    # Guardar columnas donde el producto vendido sea recargas
    sicar_recargas = archivoSICAR[archivoSICAR['Producto'].isin(['Recargas'])]
    sicar_recargas['¿Recarga registrada?'] = np.where(sicar_recargas['Producto'] == "Recargas", False, True)
    sicar_recargas = sicar_recargas.drop(columns=['Producto'])

    #Total de recargas
    totalRecargas = sicar_recargas["Total_Registrado"].sum()

    # Asignar index nuevo
    sicar_recargas.index = range(1, len(sicar_recargas) + 1)

    # Agregar columna de verificación
    st.data_editor(
        sicar_recargas,
        column_config={
            "¿Recarga registrada?": st.column_config.CheckboxColumn(
                "¿Recarga registrada?",
                help="Marca si la recarga si fue registrada",
                default=False
            )
        },
        disabled=["Total_Registrado", "Fecha", "Usuario"],
        hide_index=True,
        width=800
    )

    st.write("Total recargas: ", totalRecargas)
