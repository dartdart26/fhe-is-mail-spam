// Copyright 2021 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Modifications Copyright (C) 2021 Dart Dart

#include <stdint.h>

#include <iostream>

#include "tfhe/tfhe.h"
#include "transpiler/data/fhe_data.h"
#include "xls/common/logging/logging.h"

#ifdef USE_INTERPRETED_TFHE
#include "transpiler/examples/is_mail_spam/is_mail_spam_interpreted_tfhe.h"
#else
#include "transpiler/examples/is_mail_spam/is_mail_spam_tfhe.h"
#endif

#include "is_mail_spam.h"

static const auto main_minimum_lambda = 120;

int main(int argc, char** argv) {
  if (argc < 2) {
    std::cerr << "Error: missing mail" << std::endl;
    std::cerr << "Usage: is_mail_spam \"mail contents\"" << std::endl;
    return -1;
  }

  // generate a keyset
  auto params = new_default_gate_bootstrapping_parameters(main_minimum_lambda);

  // generate a random key
  // Note: In real applications, a cryptographically secure seed needs to be
  // used.
  uint32_t seed[] = {314, 1592, 657};
  tfhe_random_generator_setSeed(seed, 3);
  const auto key = new_random_gate_bootstrapping_secret_keyset(params);
  const auto cloud_key = &key->cloud;

  // create an input (the email) on the client side
  auto mail = std::string{argv[1]};
  mail.resize(kMaxMailSize, '\0');
  // encrypt the email on the client side
  auto mail_ciphertext = FheString::Encrypt(mail, key);
  std::cout << "[Client] Mail encryption done" << std::endl << std::endl;

  // perform mail spam detection on the server side
  std::cout << "\t\t\t\t\t[Server] Computing" << std::endl;
  auto cipher_result = FheInt{params};
  XLS_CHECK_OK(isMailSpam(cipher_result.get(), mail_ciphertext.get(), cloud_key));
  std::cout << "\t\t\t\t\t[Server] Computation done" << std::endl;

  // decrypt the result on the client side
  const auto is_spam = cipher_result.Decrypt(key);
  std::cout << "[Client] Decrypted result: " << is_spam << std::endl;
  if (is_spam) {
    std::cout << "[Client] Mail is spam!" << std::endl;
  } else {
    std::cout << "[Client] Mail is not spam." << std::endl;
  }

  return 0;
}
