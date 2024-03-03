{% macro rede(tp_rede) %}
    CASE
        WHEN {{ tp_rede }} = 1 THEN 'Pública'
        WHEN {{ tp_rede }} = 2 THEN 'Privada'
        ELSE 'Não identificado'
    END
{% endmacro %}