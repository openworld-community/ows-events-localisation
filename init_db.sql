CREATE TABLE public.translation_result
(
    source_text text NOT NULL,
    target_language character varying(5) NOT NULL,
    translated_text text,
    create_date date NOT NULL DEFAULT CURRENT_DATE,
    last_access_date date NOT NULL DEFAULT CURRENT_DATE
);

ALTER TABLE IF EXISTS public.translation_result
    OWNER to root;