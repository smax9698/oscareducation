from django import template

from student.views import get_tab_recommended_skill

register = template.Library()

@register.filter
def keep_unfinished_tests(teststudent_set_all):
  return teststudent_set_all.filter(finished_at__isnull=True)


@register.filter
def strip_untested_skills(level_list):
  return [x for x in level_list if x.tested or x.acquired]


@register.filter
def remove_closed_tests(teststudent_set):
    return teststudent_set.filter(test__running=True, test__enabled=True)

@register.simple_tag(takes_context=True)
def get_tab_recommended_skill_tag(context, of_keyword,student_skills, as_keyword, target_name):
    context[target_name] = get_tab_recommended_skill(student_skills)
    return ""
