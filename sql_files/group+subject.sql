SELECT foo.name, COUNT(foo.name) FROM
(SELECT public.group.name, count(public.group.name) FROM public.group
INNER JOIN public.subject ON public.subject.group_id=public.group.id
GROUP BY public.subject.name, public.group.name) AS foo
GROUP BY foo.name
ORDER BY count DESC
