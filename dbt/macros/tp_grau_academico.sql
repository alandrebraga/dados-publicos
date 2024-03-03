{% macro grau_academico(tp_grau_academico) %}
    CASE
        WHEN {{ tp_grau_academico }} = 1 THEN 'Bacharelado'
        WHEN {{ tp_grau_academico }} = 2 THEN 'Licenciatura'
        WHEN {{ tp_grau_academico }} = 3 THEN 'Tecnológico'
        WHEN {{ tp_grau_academico }} = 4 THEN 'Bacharelado e Licenciatura'
        ELSE 'Não identificado'
    END
{% endmacro %}