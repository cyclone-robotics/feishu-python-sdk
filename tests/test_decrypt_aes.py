#!/usr/bin/env python
# -*- coding: utf-8 -*-
from feishu.apis.base import decrypt_aes


def test_decrypt_aes():
    encrypted = "FIAfJPGRmFZWkaxPQ1XrJZVbv2JwdjfLk4jx0k/U1deAqYK3AXOZ5zcHt/cC4ZNTqYwWUW/EoL+b2hW/C4zoAQQ5CeMtbxX2zHjm+E4nX/Aww+FHUL6iuIMaeL2KLxqdtbHRC50vgC2YI7xohnb3KuCNBMUzLiPeNIpVdnYaeteCmSaESb+AZpJB9PExzTpRDzCRv+T6o5vlzaE8UgIneC1sYu85BnPBEMTSuj1ZZzfdQi7ZW992Z4dmJxn9e8FL2VArNm99f5Io3c2O4AcNsQENNKtfAAxVjCqc3mg5jF0nKabA+u/5vrUD76flX1UOF5fzJ0sApG2OEn9wfyPDRBsApn9o+fceF9hNrYBGsdtZrZYyGG387CGOtKsuj8e2E8SNp+Pn4E9oYejOTR+ZNLNi+twxaXVlJhr6l+RXYwEiMGQE9zGFBD6h2dOhKh3W84p1GEYnSRIz1+9/Hp66arjC7RCrhuW5OjCj4QFEQJiwgL45XryxHtiZ7JdAlPmjVsL03CxxFZarzxzffryrWUG3VkRdHRHbTsC34+ScoL5MTDU1QAWdqUC1T7xT0lCvQELaIhBTXAYrznJl6PlA83oqlMxpHh0gZBB1jFbfoUr7OQbBs1xqzpYK6Yjux6diwpQB1zlZErYJUfCqK7G/zI9yK/60b4HW0k3M+AvzMcw="
    result = decrypt_aes("kudryavka", encrypted)
    assert result == {'uuid': '5226cd85b4d843dccee2e279d93f3ed3',
                      'event': {'app_id': 'cli_9e28cb7ba56a100e',
                                'before_status': {'is_active': True,
                                                  'is_frozen': True,
                                                  'is_resigned': False},
                                'change_time': '2020-05-20 18:33:25',
                                'current_status': {'is_active': True,
                                                   'is_frozen': False,
                                                   'is_resigned': False},
                                'employee_id': '75ge6c49', 'open_id':
                                    'ou_2ef04637d933f798dcb92c99e845ed09',
                                'tenant_key': '2d520d3b434f175e',
                                'type': 'user_status_change'},
                      'token': 'GzhQEyfUcx7eEungQFWtXgCbxSpUOJIb',
                      'ts': '1589970805.376395',
                      'type': 'event_callback'}


if __name__ == "__main__":
    test_decrypt_aes()
