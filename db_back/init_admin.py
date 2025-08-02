"""Adding admin to the prod db if there's no anyone"""

from db_back.check_or_prompt_admin import check_or_prompt_admin

if __name__ == "__main__":
    check_or_prompt_admin()
