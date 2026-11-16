#################################################################################
#  Copyright (c) 2026 Contributors to the Eclipse Foundation
#
#  See the NOTICE file(s) distributed with this work for additional
#  information regarding copyright ownership.
#
#  This program and the accompanying materials are made available under the
#  terms of the Apache License, Version 2.0 which is available at
#  https://www.apache.org/licenses/LICENSE-2.0.
#
#  This program is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
#  AI Disclosure: This file was entirely AI-generated.
#  The AI-generated portions are made available under CC0-1.0 and not subject
#  to the project's license. The human contributor has reviewed and verified
#  that the code is correct.
#
#  SPDX-License-Identifier: Apache-2.0 AND CC0-1.0
#  Assisted-By: GitHub Copilot (Claude Sonnet 5.5)
#################################################################################
"""Path-specific HTTP controllers for C2-M3."""

from .companies.technical_users.controller import router as company_technical_users
from .internal.technical_roles.controller import router as internal_technical_roles
from .internal.technical_users.controller import router as internal_technical_users
from .osp.technical_users.controller import router as osp_technical_users
from .steps.controller import router as steps

from .companies.technical_users import PATH as COMPANY_TECHNICAL_USERS_PATH
from .internal.technical_roles import PATH as INTERNAL_TECHNICAL_ROLES_PATH
from .internal.technical_users import PATH as INTERNAL_TECHNICAL_USERS_PATH
from .osp.technical_users import PATH as OSP_TECHNICAL_USERS_PATH
from .steps import PATH as STEPS_PATH

controllers = (
    (COMPANY_TECHNICAL_USERS_PATH, company_technical_users),
    (OSP_TECHNICAL_USERS_PATH, osp_technical_users),
    (INTERNAL_TECHNICAL_USERS_PATH, internal_technical_users),
    (INTERNAL_TECHNICAL_ROLES_PATH, internal_technical_roles),
    (STEPS_PATH, steps),
)