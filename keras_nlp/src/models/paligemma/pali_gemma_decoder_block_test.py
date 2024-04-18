# Copyright 2023 The KerasNLP Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pytest

from keras_nlp.src.models.paligemma.pali_gemma_decoder_block import (
    PaliGemmaDecoderBlock,
)
from keras_nlp.src.tests.test_case import TestCase


@pytest.mark.keras_3_only
class PaliGemmaDecoderBlockTest(TestCase):
    def test_paligemma_attention_mask_computation(self):
        batch_size = 4
        img_sequence_length = 8
        text_sequence_length = 8
        total_sequence_length = img_sequence_length + text_sequence_length
        hidden_dim = 64

        decoder_block = PaliGemmaDecoderBlock(
            img_sequence_length, hidden_dim, 64, 64, 8, 8
        )

        dummy_input = np.random.rand(
            batch_size, total_sequence_length, hidden_dim
        )

        attn_mask = decoder_block._compute_attention_mask(
            dummy_input, None, None, 0
        )

        expected_mask = np.zeros(
            (batch_size, total_sequence_length, total_sequence_length)
        )
        for i in range(total_sequence_length):
            causality_index = (
                img_sequence_length if i + 1 < img_sequence_length else i + 1
            )
            expected_mask[:, i, :causality_index] = 1

        self.assertAllEqual(
            expected_mask,
            attn_mask,
        )
