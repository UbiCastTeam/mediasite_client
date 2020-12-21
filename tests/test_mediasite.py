import os
import logging
from decouple import config
from unittest import TestCase
from mediasite_client import script


class MediaSiteTest(TestCase):
    def setUp(self):
        self.EXAMPLE_PREZ = {
            'presentation': {
                'odata.id': 'https://acc.lecturenet.uu.nl/Site1/Api/v1/Presentations(\'fcb1028cce9141b884a84001d7c5b9751d\')',
                'Id': 'fcb1028cce9141b884a84001d7c5b9751d',
                'Title': 'Lezing Prof. Joanna Bourke 08-06',
                'Status': 'Viewable',
                'Source': 'HardwareRecorder',
                'RootId': 'fcb1028cce9141b884a84001d7c5b9751d',
                'RootOwner': 'm.cohen',
                'RegistrationRequired': False,
                'CurrentlyAvailableInShowcase': None,
                'ViewableByPlaylistOwner': None
            },
            'video': {
                'value': [
                    {
                        'odata.id': 'https://acc.lecturenet.uu.nl/Site1/Api/v1/Presentations(\'fcb1028cce9141b884a84001d7c5b9751d\')/OnDemandContent',
                        'Id': '9878f3bb272f487a8a7900d082a3bfc430',
                        'ParentResourceId': 'fcb1028cce9141b884a84001d7c5b9751d',
                        'ContentType': 'OnDemandFile',
                        'Status': 'Completed',
                        'ContentMimeType': 'video/mp4',
                        'EncodingOrder': 2,
                        'Length': '3034030',
                        'FileNameWithExtension': '227a7857-f901-4c5e-a26b-133e16de74eb.mp4',
                        'ContentEncodingSettingsId': 'df0db194bdbd4ac897ef7c71592fb36d28',
                        'ContentServerId': 'ad0fce8edc61432998839c3f860b6d4429',
                        'ArchiveType': 0,
                        'IsTranscodeSource': false,
                        'ContentRevision': 1,
                        'FileLength': '99688040',
                        'StreamType': 'Video1',
                        'LastModified': '2013-05-12T23:15:11.157Z'
                    },
                    {
                        'odata.id': 'https://acc.lecturenet.uu.nl/Site1/Api/v1/Presentations(\'fcb1028cce9141b884a84001d7c5b9751d\')/OnDemandContent',
                        'Id': 'ae58ff6a2eed4f04a925514b097f28d930',
                        'ParentResourceId': 'fcb1028cce9141b884a84001d7c5b9751d',
                        'ContentType': 'OnDemandFile',
                        'Status': 'Completed',
                        'ContentMimeType': 'video/x-ms-wmv',
                        'EncodingOrder': 3,
                        'Length': '3034030',
                        'FileNameWithExtension': 'fcb1028c-ce91-41b8-84a8-4001d7c5b975.wmv',
                        'ContentEncodingSettingsId': 'ea1eb6d49c11444ab420c6c3516807c128',
                        'ContentServerId': '5575446a573141d4b3fc32d51a8c860929',
                        'ArchiveType': 0,
                        'IsTranscodeSource': true,
                        'ContentRevision': 1,
                        'FileLength': '300287839',
                        'StreamType': 'Video1',
                        'LastModified': '2013-05-12T23:15:12.733Z'
                    }
                ]
            },
            'slides': {
                'odata.id': 'https://acc.lecturenet.uu.nl/Site1/Api/v1/Presentations(\'fcb1028cce9141b884a84001d7c5b9751d\')/SlideDetailsContent',
                'SlideDetails': [
                    {
                        'TimeMilliseconds': 627,
                        'Number': 1,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'Historical Reflections, 1760s to 1960s '
                    },
                    {
                        'TimeMilliseconds': 299602,
                        'Number': 2,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'Margaret Edson \'s W. \'I have been asked `How are you feeling today?' while I was throwing up into a plastic washbasin. I have been asked as I was emerging from a four-hour operation with a tube in every orifice, 'How are you feeling today?' I am waiting for the moment when someone asks me this question and I am dead. I'm a little sorry Ill miss that.\' '
                    },
                    {
                        'TimeMilliseconds': 379226,
                        'Number': 3,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'Elaine Scarry Pain \'is not of  or for anything. It is precisely because it takes no object that it, more than any other phenomenon, resists objectification in language.\' '
                    },
                    {
                        'TimeMilliseconds': 577166,
                        'Number': 4,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'Harriet Martineau \'Where are these pains now? — Not only gone, but annihilated.... This pain, which I feel now as I write, I have felt innumerable times before.... and a few hours hence I shall be as unable to represent it to myself as to the healthiest person in the house.\' (1844) '
                    },
                    {
                        'TimeMilliseconds': 646649,
                        'Number': 5,
                        'Title': null,
                        'Content': null,
                        'OcrText': ''
                    },
                    {
                        'TimeMilliseconds': 670756,
                        'Number': 6,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'Fanny Burney August 1812 When \'the dreadful steel was plunged into the breast cutting through veins — arteries — flesh nerves... I began a scream that lasted intermittingly during the whole time of the incident.... for Months I could not speak of this terrible business without nearly again going through it!\' '
                    },
                    {
                        'TimeMilliseconds': 981111,
                        'Number': 7,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'et — *mat SAAB ghe Cho& ccriernit4&Citrainjerf-issaiil '
                    },
                    {
                        'TimeMilliseconds': 1291631,
                        'Number': 8,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'Image schemata created from sensorimotor bodily experiences a BALANCE: \'pain weighed down her spirits\' • DIFFICULTIES ARE BURDENS: \'the pain weighed her down\' • IMPORTANCE IS BIG: \'the ache in her stomach grew by the minute\' • MORE IS UP: \'her pain soared\' • STATES ARE LOCATIONS: \'she was close to screaming\' a CHANGE IS MOTION: \'the pain went from bad to worse\' a PHYSICAL AND EMOTIONAL STATES ARE EN I II 1ES WITHIN A PERSON: \'her pain went away\' a INTENSITY IS HEAT: \'the tumour burned fiercely\' '
                    },
                    {
                        'TimeMilliseconds': 1453634,
                        'Number': 9,
                        'Title': null,
                        'Content': null,
                        'OcrText': ''
                    },
                    {
                        'TimeMilliseconds': 1535318,
                        'Number': 10,
                        'Title': null,
                        'Content': null,
                        'OcrText': ''
                    },
                    {
                        'TimeMilliseconds': 1612831,
                        'Number': 11,
                        'Title': null,
                        'Content': null,
                        'OcrText': '4 -4(cri-stri '
                    },
                    {
                        'TimeMilliseconds': 1746298,
                        'Number': 12,
                        'Title': null,
                        'Content': null,
                        'OcrText': '\'I have seen the most heroic and stout-hearted men shed tears like a child, when enduring the agony of neuralgia. As in a powerful engine when the director turns some little key, and the monster is at once aroused, and plunges along the pathway, screaming and breathing forth flames in the majesty of his power, so the hero of a hundred battles, if perchance a filament of nerve is compressed, is seized with spasms, and struggles to escape the unendurable agony\'. (1862) '
                    },
                    {
                        'TimeMilliseconds': 1836382,
                        'Number': 13,
                        'Title': null,
                        'Content': null,
                        'OcrText': ''
                    },
                    {
                        'TimeMilliseconds': 1889184,
                        'Number': 14,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'Virginia Woolf \'English, which can express the thoughts of Hamlet and the tragedy of Lear, has no words for the shiver and the headache.... The merest schoolgirl, when she falls in love, has Shakespeare and Keats to speak her mind for her; but let a sufferer try to describe a pain in his head to a doctor and language at once runs dry\' (1930) ON BEING ILL •11111••••11•111•11•11•8011 oess•••11 0000000000 • ...Os OVEN oo • •110••••11111•11•1111•11•• 00111•11116••••••••o■ OOOOO •••••••••••••• Ili•••••••••••••1111s• IB1111811111•1111110111 OOOOO 1111111111111111111••••••■111111:■ OOOOO .••■•••• aim sesommoss. esilis•WIlla•••••011 01111101111111111111111161111 01111,0111111111111111118111111 ■ilmall••••01111111111111 ■1111111101111111111111111111111■ ••• '
                    },
                    {
                        'TimeMilliseconds': 2095120,
                        'Number': 15,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'staitkei 11004 Ada nces742 iftWiffdll ephfrim, CA, cahriniivostgistend.i. sOshora 444 YR Ca b-4 • is ;,-37-4, r4 4_7,- .4 hi zieme,;t.,, A intiyol '
                    },
                    {
                        'TimeMilliseconds': 2098253,
                        'Number': 16,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'The Humours: the body consisted of four fluids phlegm, black bile, yellow bile, and blood. '
                    },
                    {
                        'TimeMilliseconds': 2137022,
                        'Number': 17,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'Humoural Descriptions of Pain (1731) Her blood was \'too glutinous and weak to perform its proper circulation, stops at every narrow passage in its progress, causes exquisite pains in all the little, irritated, distended vessels of the body, produces tumours in those that stretch most easily, and keeps the stomach and bowels constantly clogged.\' '
                    },
                    {
                        'TimeMilliseconds': 2254004,
                        'Number': 18,
                        'Title': null,
                        'Content': null,
                        'OcrText': ''
                    },
                    {
                        'TimeMilliseconds': 2303411,
                        'Number': 19,
                        'Title': null,
                        'Content': null,
                        'OcrText': ''
                    },
                    {
                        'TimeMilliseconds': 2412139,
                        'Number': 20,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'Adam Smith Through acts of imagination, \'we place ourselves in his situation, we conceive ourselves enduring all the same torments, we enter as it were into his body, and become in some measure the same person with him, and thence form some idea of his sensations, and even feel something which, though weaker in degree, is not altogether unlike them\' (1759). '
                    },
                    {
                        'TimeMilliseconds': 2686631,
                        'Number': 21,
                        'Title': null,
                        'Content': null,
                        'OcrText': ''
                    },
                    {
                        'TimeMilliseconds': 2740506,
                        'Number': 22,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'William Osier 1904 \'Keen sensibility is doubtless a virtue of high order... but for the practitioner in his working-day world, a callousness which thinks only of the good to be effected, and goes ahead regardless of smaller considerations, is the preferable quality.\' '
                    },
                    {
                        'TimeMilliseconds': 2826509,
                        'Number': 23,
                        'Title': null,
                        'Content': null,
                        'OcrText': 'Treaty of Utrecht Chair (2011) Pain and the Politics of Sympathy: Historical Reflections, 1760s to 1960s Joanna Bourke '
                    }
                ],
                'Id': 'b8af944a19874e4eae025ea48ab7fa7a30',
                'ParentResourceId': 'fcb1028cce9141b884a84001d7c5b9751d',
                'ContentType': 'Slides',
                'Status': 'Completed',
                'ContentMimeType': 'image/jpeg',
                'EncodingOrder': 1,
                'Length': '23',
                'FileNameWithExtension': 'slide_{0:D4}_full.jpg',
                'ContentEncodingSettingsId': '07b772d1f0af4bb9986f64d26ee1b0e228',
                'ContentServerId': '2127f2fa7dee41aba6cf64c777e5611829',
                'ArchiveType': 0,
                'IsTranscodeSource': False,
                'ContentRevision': 1,
                'FileLength': '2708112',
                'StreamType': 'Slide',
                'LastModified': '2013-05-12T23:15:09.953Z'
            }
        }
